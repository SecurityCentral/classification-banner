#
# Copyright (C) 2018 SecurityCentral Contributors. See LICENSE for license
#

import sys
import os
import argparse
import time
import configparser
from socket import gethostname
from distutils.util import strtobool

# Global Configuration File
CONF_FILE = "/etc/classification-banner/banner.conf"


# Check if DISPLAY variable is set
try:
    os.environ["DISPLAY"]
except KeyError:
    print("Error: DISPLAY environment variable is not set.")
    sys.exit(1)

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
except ImportError as e:
    raise e


def get_user():
    """Returns Username"""
    try:
        user = os.getlogin()
    except OSError:
        user = ''

    return user


def get_host():
    """Returns Hostname"""
    host = gethostname()
    host = host.split('.')[0]
    return host


def configure():
    """Read Global configuration"""
    defaults = {}
    defaults["message"] = "UNCLASSIFIED"
    defaults["foreground"] = "#FFFFFF"
    defaults["background"] = "#007A33"
    defaults["font"] = "liberation-sans"
    defaults["size"] = "small"
    defaults["weight"] = "bold"
    defaults["show_top"] = "True"
    defaults["show_bottom"] = "True"
    defaults["horizontal_resolution"] = 0
    defaults["vertical_resolution"] = 0
    defaults["sys_info"] = "False"
    defaults["opacity"] = 0.75
    defaults["esc"] = "True"
    defaults["spanning"] = "False"

    conf = configparser.ConfigParser()
    conf.read(CONF_FILE)
    for key, val in conf.items("global"):
        defaults[key] = val

    # Use the global config to set defaults for command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", default=defaults["message"],
                        help="Set the Classification message")
    parser.add_argument("-f", "--fgcolor", default=defaults["foreground"],
                        help="Set the Foreground (text) color")
    parser.add_argument("-b", "--bgcolor", default=defaults["background"],
                        help="Set the Background color")
    parser.add_argument("-x", "--hres", default=defaults["horizontal_resolution"], type=int,
                        help="Set the Horizontal Screen Resolution")
    parser.add_argument("-y", "--vres", default=defaults["vertical_resolution"], type=int,
                        help="Set the Vertical Screen Resolution")
    parser.add_argument("-o", "--opacity", default=defaults["opacity"],
                        type=float, dest="opacity",
                        help="Set the window opacity for composted window managers")
    parser.add_argument(
            "--font", default=defaults["font"], help="Font type")
    parser.add_argument(
            "--size", default=defaults["size"], help="Font size")
    parser.add_argument("--weight", default=defaults["weight"],
                        help="Set the Font weight")
    parser.add_argument("--disable-esc", default=strtobool(defaults["esc"]),
                        dest="esc", action="store_false",
                        help="Disable the 'ESC to hide' message")
    parser.add_argument("--hide-top", default=strtobool(defaults["show_top"]),
                        dest="show_top", action="store_false",
                        help="Disable the top banner")
    parser.add_argument("--hide-bottom", default=strtobool(defaults["show_bottom"]),
                        dest="show_bottom", action="store_false",
                        help="Disable the bottom banner")
    parser.add_argument("--system-info", default=strtobool(defaults["sys_info"]),
                        dest="sys_info", action="store_true",
                        help="Show user and hostname in the top banner")
    parser.add_argument("--enable-spanning", default=strtobool(defaults["spanning"]),
                        dest="spanning", action="store_true",
                        help="Enable banner(s) to span across screens as a single banner")

    args = parser.parse_args()

    return args


# Classification Banner Class
class ClassificationBanner:
    """Class to create and refresh the actual banner."""

    def __init__(self, message="UNCLASSIFIED", fgcolor="#FFFFFF",
                 bgcolor="#007A33", font="liberation-sans", size="small",
                 weight="bold", x=0, y=0, esc=True, opacity=0.75,
                 sys_info=False):
        """Set up and display the main window

        Keyword arguments:
        message -- The classification level to display
        fgcolor -- Foreground color of the text to display
        bgcolor -- Background color of the banner the text is against
        font    -- Font type to use for the displayed text
        size    -- Size of font to use for text
        weight  -- Bold or normal
        hres    -- Horizontal Screen Resolution (int) [ requires vres ]
        vres    -- Vertical Screen Resolution (int) [ requires hres ]
        opacity -- Opacity of window (float) [0 .. 1, default 0.75]
        """
        self.hres = x
        self.vres = y
        # pylint: disable=consider-using-f-string
        self.css = """window label {
          background-color: %s;
}
""" % bgcolor

        # Dynamic Resolution Scaling
        self.monitor = Gdk.Screen()
        self.monitor.connect("size-changed", self.resize)

        # Newer versions of pygtk have this method
        try:
            self.monitor.connect("monitors-changed", self.resize)
        except AttributeError:
            pass

        # Create Main Window
        self.window = Gtk.Window()
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("hide", self.restore)
        self.window.connect("key-press-event", self.keypress)
        self.window.set_property('skip-taskbar-hint', True)
        self.window.set_property('skip-pager-hint', True)
        self.window.set_property('destroy-with-parent', True)
        self.window.stick()
        self.window.set_decorated(False)
        self.window.set_keep_above(True)
        self.window.set_app_paintable(True)

        # Set the default window size
        self.window.set_default_size(int(self.hres), 5)

        # Create Main Horizontal Box to Populate
        self.hbox = Gtk.HBox()

        # Create the Center Vertical Box
        self.vbox_center = Gtk.VBox()
        # pylint: disable=consider-using-f-string
        self.center_label = Gtk.Label(
            "<span font_family='%s' weight='%s' foreground='%s' size='%s'>%s</span>" %
            (font, weight, fgcolor, size, message))
        self.center_label.set_use_markup(True)
        self.center_label.set_justify(Gtk.Justification.CENTER)
        self.vbox_center.pack_start(self.center_label, True, True, 0)

        # Create the Right-Justified Vertical Box to Populate for hostname
        self.vbox_right = Gtk.VBox()
        # pylint: disable=consider-using-f-string
        self.host_label = Gtk.Label(
            "<span font_family='%s' weight='%s' foreground='%s' size='%s'>%s</span>" %
            (font, weight, fgcolor, size, get_host()))
        self.host_label.set_use_markup(True)
        self.host_label.set_justify(Gtk.Justification.RIGHT)
        self.host_label.set_width_chars(20)

        # Create the Left-Justified Vertical Box to Populate for user
        self.vbox_left = Gtk.VBox()
        # pylint: disable=consider-using-f-string
        self.user_label = Gtk.Label(
            "<span font_family='%s' weight='%s' foreground='%s' size='%s'>%s</span>" %
            (font, weight, fgcolor, size, get_user()))
        self.user_label.set_use_markup(True)
        self.user_label.set_justify(Gtk.Justification.LEFT)
        self.user_label.set_width_chars(20)

        # Create the Right-Justified Vertical Box to Populate for ESC message
        self.vbox_esc_right = Gtk.VBox()
        # pylint: disable=line-too-long,consider-using-f-string
        self.esc_label = Gtk.Label(label="<span font_family='liberation-sans' weight='normal' foreground='%s' size='xx-small'>  (ESC to hide temporarily)  </span>" %  # noqa: E501
                                   (fgcolor))
        self.esc_label.set_use_markup(True)
        self.esc_label.set_justify(Gtk.Justification.RIGHT)
        self.esc_label.set_width_chars(20)

        # Empty Label for formatting purposes
        self.vbox_empty = Gtk.VBox()
        self.empty_label = Gtk.Label(
            label="<span font_family='liberation-sans' weight='normal'>                 </span>")
        self.empty_label.set_use_markup(True)
        self.empty_label.set_width_chars(20)

        if not esc:
            if not sys_info:
                self.hbox.pack_start(self.vbox_center, True, True, 0)
            else:
                self.vbox_right.pack_start(self.host_label, True, True, 0)
                self.vbox_left.pack_start(self.user_label, True, True, 0)
                self.hbox.pack_start(self.vbox_right, False, True, 20)
                self.hbox.pack_start(self.vbox_center, True, True, 0)
                self.hbox.pack_start(self.vbox_left, False, True, 20)

        else:
            if esc and not sys_info:
                self.empty_label.set_justify(Gtk.Justification.LEFT)
                self.vbox_empty.pack_start(self.empty_label, True, True, 0)
                self.vbox_esc_right.pack_start(self.esc_label, True, True, 0)
                self.hbox.pack_start(self.vbox_esc_right, False, True, 0)
                self.hbox.pack_start(self.vbox_center, True, True, 0)
                self.hbox.pack_start(self.vbox_empty, False, True, 0)

        if sys_info:
            self.vbox_right.pack_start(self.host_label, True, True, 0)
            self.vbox_left.pack_start(self.user_label, True, True, 0)
            self.hbox.pack_start(self.vbox_right, False, True, 20)
            self.hbox.pack_start(self.vbox_center, True, True, 0)
            self.hbox.pack_start(self.vbox_left, False, True, 20)

        self.window.add(self.hbox)
        self.window.show_all()
        self.width, self.height = self.window.get_size()
        # load style from file
        provider = Gtk.CssProvider()
        provider.load_from_data(self.css.encode())
        self.apply_css(self.window, provider)

        try:
            self.window.set_opacit(opacity)
        except AttributeError:  # nosec
            pass

    def apply_css(self, widget, provider):
        """Apply CSS to window"""
        Gtk.StyleContext.add_provider(widget.get_style_context(),
                                      provider,
                                      Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        if isinstance(widget, Gtk.Container):
            widget.forall(self.apply_css, provider)

    def restore(self):
        """Restore Minimized Window"""
        self.window.deiconify()
        self.window.present()

        return True

    def resize(self):
        """Destroy Classification Banner Window on Resize (Display Banner Will Relaunch)"""
        self.window.destroy()

        return True

    def keypress(self, event=None):
        """Press ESC to hide window for 15 seconds"""
        if event.keyval == 65307:
            if not Gtk.events_pending():
                self.window.iconify()
                self.window.hide()
                time.sleep(15)
                self.window.show()
                self.window.deiconify()
                self.window.present()

        return True


class DisplayBanner:
    """Display Classification Banner Message"""

    def __init__(self):
        """Dynamic Resolution Scaling"""
        self.monitor = Gdk.Screen()
        self.monitor.connect("size-changed", self.resize)

        # Newer versions of pygtk have this method
        try:
            self.monitor.connet("monitors-changed", self.resize)
        except AttributeError:
            pass

        # Launch Banner
        self.config = configure()
        self.execute(self.config)

    def execute(self, options):
        """Launch the Classification Banner Window(s)"""
        self.num_monitor = 0

        if options.hres == 0 or options.vres == 0:
            # Try Xrandr to determine primary monitor resolution
            try:
                self.screen = os.popen(  # nosec
                    "/usr/bin/xrandr | grep ' connected ' | awk '{ print $3 }'").readlines()[0]
                self.x = self.screen.split('x')[0]
                self.y = self.screen.split('x')[1].split('+')[0]

            except IndexError:
                try:
                    self.screen = os.popen(  # nosec
                        "/usr/bin/xrandr | grep ' current ' | awk '{ print $8$9$10+0 }'").readlines()[0]
                    self.x = self.screen.split('x')[0]
                    self.y = self.screen.split('x')[1].split('+')[0]

                except IndexError:
                    self.screen = os.popen(  # nosec
                        r"/usr/bin/xrandr | grep '^\*0' | awk '{ print $2$3$4 }'").readlines()[0]
                    self.x = self.screen.split('x')[0]
                    self.y = self.screen.split('x')[1].split('+')[0]

                else:
                    # Fail back to GTK method
                    self.display = Gdk.Display.get_default()
                    self.screen = self.display.get_default_screen()
                    self.x = self.screen.get_width()
                    self.y = self.screen.get_height()
        else:
            # Resoultion Set Staticly
            self.x = options.hres
            self.y = options.vres

        if not options.spanning and self.num_monitor > 1:
            for monitor in range(self.num_monitor):
                mon_geo = self.screen.get_monitor_geometry(monitor)
                self.x_location, self.y_location, self.x, self.y = mon_geo
                self.banners(options)
        else:
            self.x_location = 0
            self.y_location = 0
            self.banners(options)

    def banners(self, options):
        """Set banner configuration"""
        if options.show_top:
            top = ClassificationBanner(
                options.message,
                options.fgcolor,
                options.bgcolor,
                options.font,
                options.size,
                options.weight,
                self.x,
                self.y,
                options.esc,
                options.opacity,
                options.sys_info)
            top.window.move(self.x_location, self.y_location)

        if options.show_bottom:
            bottom = ClassificationBanner(
                options.message,
                options.fgcolor,
                options.bgcolor,
                options.font,
                options.size,
                options.weight,
                self.x,
                self.y,
                options.esc,
                options.opacity)
            bottom.window.move(self.x_location, int(bottom.vres))

    def resize(self):
        """Relaunch the Classification Banner on Screen Resize"""
        self.config = configure()
        self.execute(self.config)

        return True


def main():
    """Display Banner"""
    DisplayBanner()
    Gtk.main()

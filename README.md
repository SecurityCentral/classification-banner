Classification-Banner
=====================

<a href="https://scan.coverity.com/projects/securitycentral-classification-banner">
  <img alt="Coverity Scan Build Status"
       src="https://img.shields.io/coverity/scan/16706.svg"/>
</a>

Classification Banner is a python script that will display the
classification level banner of a session with a variety of
configuration options on the primary screen.  This script can
help government and possibly private customers display a
notification that sensitive material is being displayed - for
example PII or SECRET Material being processed in a graphical
session. The script has been tested on a variety of graphical
environments such as GNOME2, GNOME3, KDE, twm, icewm, and Cinnamon.

Python script verified working on Red Hat Enterprise Linux and Fedora.

Selecting the classification window and pressing the ESC key
will temporarily hide the window for 15 seconds, it will return
to view after that

Installation
============

## Fedora
`classification-banner` can be found in the Fedora repositories and installed
via `dnf`:
```sh
dnf -y install classification-banner
```

## RHEL
`classification-banner` can be found in the [EPEL](https://fedoraproject.org/wiki/EPEL) repositories and installed
via `yum`:
```sh
yum -y install classification-banner
```

## Source
To install directly from source, run the following command:
```sh
python setup.py install
```

Classification Banner Usage
===========================

Options should be placed in the `/etc/classification-banner/banner.conf` file.

```
 message      - The classification level to display (Default: 'UNCLASSIFIED')
 foreground   - Foreground color of the text to display (Default: '#007A33' "Green")
 background   - Background color of the banner the text is against (Default: '#FFFFFF' "White")
 font         - Font face to use for the displayed text (Default: 'liberation-sans')
 size         - Size of font to use for text (Default: 'small')
 weight       - Bold or normal (Default: 'bold')
 show_top     - Show top banner (Default: True)
 show_bottom  - Show bottom banner (Default: True)
 horizontal_resolution         - Manually Set Horiztonal Resolution (OPTIONAL) [ if hres is set, vres required ]
 vertical_resolution           - Manually Set Horiztonal Resolution (OPTIONAL) [ if vres is set, hres required ]
 sys_info     - Show user and hostname in the top banner (Default: False)
 opacity      - Sets opacity - for composted window managers only (OPTIONAL) [float - range 0 .. 1] (Default 0.75)
 esc          - Enable/Disable the 'ESC to hide' message (Default: True (enabled))
 spanning     - Enable banner(s) to span across screens as a single banner (Default: False)
```

Command line options that correspond to the above settings (use `classification-banner --help` for more information):

```
 -m, --message
 -f, --fgcolor
 -b, --bgcolor
 --font
 --size
 --weight
 --hide-top
 --hide-bottom
 -x, --hres
 -y, --vres
 --system-info
 -o, --opacity
 --disable-esc
 --enable-spanning
```

Examples
========

These are examples for the configuration of the Classification Banner
using the `/etc/classification-banner/banner.conf` file for various classifications
based upon generally accepted color guidelines in the DoD/IC.

Note: The U.S. General Services Administration (GSA) no longer publishes
the color values used for printing U.S. Government Standard Forms (SF)
such as the SF-710 (Unclassified Label), SF-708 (Confidential Label),
SF-707 (Secret Label), SF-706 (Top Secret Label), or SF-712 (Classified
SCI Label): http://www.gsa.gov/portal/content/142623

However, archived copies of superseded U.S. Government documents provide
the previously published Pantone values as well as a publicly available
contract document on gpo.gov:

"GENERAL TERMS, CONDITIONS, AND SPECIFICATIONS For the Procurement of
Labels as requisitioned from the U.S. Government Publishing Office (GPO)
by the Federal Prison Industries (FPI) Unicor"; U.S. Government Publishing
Office; 28 April 2016;

https://www.gpo.gov/docs/default-source/contract-pricing/dallas/ab1724s.pdf

SF-710: Pantone 356 - (Reverse printing) White on Green
SF-708: Pantone 286 - (Reverse printing) White on Blue
SF-707: Pantone 186 - (Reverse printing) White on Red
SF-706: Pantone 165 - (Reverse printing) White on Orange
SF-712: Pantone 101 - Black on Yellow
SF-709: Pantone 264 - Black on Lavender

The following are the approximate RGB and HEX values of the above Pantone
Solid Coated values as provided by the Pantone website:

```
SF-710: RGB:   0, 122,  51 / HEX: #007a33 | https://www.pantone.com/color-finder/356-C
SF-708: RGB:   0,  51, 160 / HEX: #0033a0 | https://www.pantone.com/color-finder/286-C
SF-707: RGB: 200,  16,  46 / HEX: #c8102e | https://www.pantone.com/color-finder/186-C
SF-706: RGB: 255, 103,  31 / HEX: #ff671f | https://www.pantone.com/color-finder/165-C
SF-712: RGB: 247, 234,  72 / HEX: #f7ea48 | https://www.pantone.com/color-finder/101-C
SF-709: RGB: 193, 167, 226 / HEX: #c1a7e2 | https://www.pantone.com/color-finder/264-C

    Default (UNCLASSIFIED)

    CONFIDENTIAL

        message='CONFIDENTIAL'
        foreground='#FFFFFF'
        background='#0033A0'

    SECRET

        message='SECRET'
        foreground='#FFFFFF'
        background='#C8102E'

    TOP SECRET

        message='TOP SECRET'
        foreground='#FFFFFF'
        background='#FF671F'

    TOP SECRET//SCI

        message='TOP SECRET//SCI'
        foreground="#000000'
        background='#F7EA48'
```

Autostart
=========

To auto-start the classification-banner script on the GNOME Desktop,
create the following file:

```sh
vi /etc/xdg/autostart/classification-banner.desktop

     [Desktop Entry]
     Name=Classification Banner
     Exec=/usr/bin/classification-banner
     Comment=User Notification for Security Level of System.
     Type=Application
     Encoding=UTF-8
     Version=1.0
     MimeType=application/python;
     Categories=Utility;
     X-GNOME-Autostart-enabled=true
     StartupNotify=false
     Terminal=false
```

Name:           classification-banner
Version:        1.7.1
Release:        14.20220409223256181383.py3_egg_Test.22.gd2eb664%{?dist}
Summary:        Displays Classification Banner for a Graphical Session

License:        GPLv2+
URL:            https://github.com/SecurityCentral/classification-banner
Source0:        classification-banner-1.7.1.tar.gz

BuildArch:      noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-gobject
BuildRequires:  desktop-file-utils
BuildRequires:  gtk3
Requires:       xrandr
Requires:       python3-gobject
Requires:       gtk3

%description
Classification Banner is a python script that will display the
classification level banner of a session with a variety of
configuration options on the primary screen.  This script can
help government and possibly private customers display a 
notification that sensitive material is being displayed - for 
example PII or SECRET Material being processed in a graphical
session. The script has been tested on a variety of graphical
environments such as GNOME2, GNOME3, KDE, twm, icewm, and Cinnamon.

%prep
%autosetup -n classification-banner-1.7.1

%build
%py3_build

%install
%py3_install

install -d -m755 %{buildroot}%{_datadir}/%{name}
install -d -m755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m755 %{buildroot}%{_sysconfdir}/xdg/autostart/

install -pm644 contrib/banner.conf %{buildroot}%{_sysconfdir}/%{name}/banner.conf
install -pm644 share/%{name}-screenshot.png %{buildroot}%{_datadir}/%{name}/%{name}-screenshot.png

desktop-file-install \
--dir=%{buildroot}%{_sysconfdir}/xdg/autostart \
contrib/%{name}.desktop

%check
export DISPLAY=":0.0"
%{__python3} setup.py test

%files
%license LICENSE
%doc README.md AUTHOR Contributors.md
%{python3_sitelib}/classification_banner
%{python3_sitelib}/classification_banner-*.egg-info/

%config(noreplace) %{_sysconfdir}/%{name}/banner.conf
%config(noreplace) %{_sysconfdir}/xdg/autostart/classification-banner.desktop
%{_bindir}/%{name}
%{_datadir}/%{name}/%{name}-screenshot.png

%changelog
* Sat Apr 09 2022 Gabe <redhatrises@gmail.com> - 1.7.1-14.20220409223256181383.py3_egg_Test.22.gd2eb664
- Fix egg-info dir (Gabe)
- Fix SPEC name (Gabe)
- Add packit config (Gabe)
- Update tar handling (Gabe)
- Add release action (Gabe)
- Use GH action linting badge in readme (Gabe)
- Remove Travis CI (Gabe)
- More pylint fixes (Gabe)
- Python linting fixes and configuration (Gabe)
- Add flake8 and pylint config (Gabe)
- Update deprecated python3-isms (Gabe)
- Add python linting (Gabe)
- Add rpm spec file (Gabe)

* Sat Apr 09 2022 Gabe <redhatrises@gmail.com> - 1.7.1-14.20220409223219944840.py3_egg_Test.22.gd2eb664
- Fix egg-info dir (Gabe)
- Fix SPEC name (Gabe)
- Add packit config (Gabe)
- Update tar handling (Gabe)
- Add release action (Gabe)
- Use GH action linting badge in readme (Gabe)
- Remove Travis CI (Gabe)
- More pylint fixes (Gabe)
- Python linting fixes and configuration (Gabe)
- Add flake8 and pylint config (Gabe)
- Update deprecated python3-isms (Gabe)
- Add python linting (Gabe)
- Add rpm spec file (Gabe)

* Sat Apr 09 2022 Gabe <redhatrises@gmail.com> - 1.7.1-14.20220409223031295745.py3_egg_Test.22.gd2eb664
- Fix egg-info dir (Gabe)
- Fix SPEC name (Gabe)
- Add packit config (Gabe)
- Update tar handling (Gabe)
- Add release action (Gabe)
- Use GH action linting badge in readme (Gabe)
- Remove Travis CI (Gabe)
- More pylint fixes (Gabe)
- Python linting fixes and configuration (Gabe)
- Add flake8 and pylint config (Gabe)
- Update deprecated python3-isms (Gabe)
- Add python linting (Gabe)
- Add rpm spec file (Gabe)

* Sat Apr 09 2022 Gabe <redhatrises@gmail.com> - 1.7.0-14.20220409163004025426.py3_egg_Test
- Development snapshot (d2eb664e)


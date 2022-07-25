Name:           classification-banner
Version:        1.6.7
Release:        2%{?dist}
Summary:        Displays Classification Banner for a Graphical Session

License:        GPLv2+
URL:            https://github.com/millennialsoftware/classification-banner
Source0:        %{URL}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  pygtk2
BuildRequires:  pygobject2
BuildRequires:  desktop-file-utils
Requires:       xorg-x11-server-utils
Requires:       pygtk2
Requires:       pygobject2

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
%autosetup -p1

%build
%py2_build

%install
%py2_install

install -d -m755 %{buildroot}%{_datadir}/%{name}
install -d -m755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m755 %{buildroot}%{_sysconfdir}/xdg/autostart/

install -pm644 contrib/banner.conf %{buildroot}%{_sysconfdir}/%{name}/banner.conf
install -pm644 share/%{name}-screenshot.png %{buildroot}%{_datadir}/%{name}/%{name}-screenshot.png

desktop-file-install \
--dir=%{buildroot}%{_sysconfdir}/xdg/autostart \
contrib/%{name}.desktop

%check
%{__python2} setup.py test

%post
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :

%files
%license LICENSE
%doc README.md AUTHOR Contributors.md
%{python2_sitelib}/classification_banner
%{python2_sitelib}/classification_banner-%{version}-py?.?.egg-info

%config(noreplace) %{_sysconfdir}/%{name}/banner.conf
%config(noreplace) %{_sysconfdir}/xdg/autostart/classification-banner.desktop
%{_bindir}/%{name}
%{_datadir}/%{name}/%{name}-screenshot.png

%changelog
* Wed Feb 13 2019 Gabe <redhatrises@gmail.com> - 1.6.7-2
- Fix booleans being read as strings from banner.conf (rhbz#1669155)

* Thu Aug 9 2018 Gabe <redhatrises@gmail.com> - 1.6.7-1
- First package for EPEL

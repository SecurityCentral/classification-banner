Name:           classification-banner
Version:        1.7.1
Release:        1%{?dist}
Summary:        Displays Classification Banner for a Graphical Session

License:        GPLv2+
URL:            https://github.com/SecurityCentral/classification-banner
Source0:        %{URL}/archive/%{version}/%{name}-%{version}.tar.gz

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
%autosetup -n %{name}-%{version}

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
%{tox}

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

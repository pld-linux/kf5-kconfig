%define		kdeframever	5.67
%define		qtver		5.9.0
%define		kfname		kconfig

Summary:	Backend for storing application configuration
Name:		kf5-%{kfname}
Version:	5.67.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	3a40f76617827bff8e0c99b93be01fc1
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= %{kdeframever}
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KConfig provides an advanced configuration system. It is made of two
parts: KConfigCore and KConfigGui.

KConfigCore provides access to the configuration files themselves. It
features:

- Code generation: describe your configuration in an XML file, and use
  `kconfig_compiler to generate classes that read and write
  configuration entries.
- Cascading configuration files (global settings overridden by local
  settings).
- Optional shell expansion support (see [docs/options.md](@ref
  options)).
- The ability to lock down configuration options (see
  [docs/options.md](@ref options)).

KConfigGui provides a way to hook widgets to the configuration so that
they are automatically initialized from the configuration and
automatically propagate their changes to their respective
configuration files.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Xml-devel >= %{qtver}
Requires:	cmake >= 2.6.0

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/kconf_update
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc DESIGN README.md TODO
%attr(755,root,root) %ghost %{_libdir}/libKF5ConfigCore.so.5
%attr(755,root,root) %{_libdir}/libKF5ConfigCore.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5ConfigGui.so.5
%attr(755,root,root) %{_libdir}/libKF5ConfigGui.so.*.*
%attr(755,root,root) %{_bindir}/kreadconfig5
%attr(755,root,root) %{_bindir}/kwriteconfig5
%attr(755,root,root) %{_libexecdir}/kf5/kconf_update
%attr(755,root,root) %{_libexecdir}/kf5/kconfig_compiler_kf5
%dir %{_datadir}/kconf_update
%{_datadir}/qlogging-categories5/kconfig.categories

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5ConfigCore.so
%attr(755,root,root) %{_libdir}/libKF5ConfigGui.so
%{_includedir}/KF5/KConfigCore
%{_includedir}/KF5/KConfigGui
%{_includedir}/KF5/kconfig_version.h
%{_libdir}/cmake/KF5Config
%{qt5dir}/mkspecs/modules/qt_KConfigCore.pri
%{qt5dir}/mkspecs/modules/qt_KConfigGui.pri

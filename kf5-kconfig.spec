# TODO:
# - dir /usr/include/KF5 not packaged
%define         _state          stable
%define		orgname		kconfig

Summary:	Backend for storing application configuration
Name:		kf5-%{orgname}
Version:	5.0.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/frameworks/%{version}/%{orgname}-%{version}.tar.xz
# Source0-md5:	d7cdb25dd4645904332ef9eee71143ec
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel >= 5.3.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Xml-devel >= 5.2.0
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.0.0
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
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
Summary:	Header files for %{orgname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{orgname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{orgname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{orgname}.

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DKCFG_INSTALL_DIR=%{_datadir}/config.kcfg \
	-DPLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQT_PLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQML_INSTALL_DIR=%{qt5dir}/qml \
	-DIMPORTS_INSTALL_DIR=%{qt5dirs}/imports \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_LIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_INCLUDE_INSTALL_DIR=%{_includedir} \
	-DECM_MKSPECS_INSTALL_DIR=%{qt5dir}/mkspecs/modules \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{orgname}5_qt --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{orgname}5_qt.lang
%defattr(644,root,root,755)
%doc DESIGN README.md TODO
%attr(755,root,root) %ghost %{_libdir}/libKF5ConfigCore.so.5
%attr(755,root,root) %{_libdir}/libKF5ConfigCore.so.5.0.0
%attr(755,root,root) %ghost %{_libdir}/libKF5ConfigGui.so.5
%attr(755,root,root) %{_libdir}/libKF5ConfigGui.so.5.0.0
%attr(755,root,root) %{_bindir}/kconfig_compiler_kf5
%attr(755,root,root) %{_bindir}/kreadconfig5
%attr(755,root,root) %{_bindir}/kwriteconfig5
%attr(755,root,root) %{_libdir}/kf5/kconf_update

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

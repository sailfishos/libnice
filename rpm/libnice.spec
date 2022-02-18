Name:       libnice
Summary:    GLib ICE implementation
Version:    0.1.17
Release:    1
License:    LGPLv2 and MPLv1.1
URL:        https://libnice.freedesktop.org/
Source0:    %{name}-%{version}.tar.bz2
Patch0:     nemo-tests-install.patch
Patch1:     0001-Add-mktests.sh.patch
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  meson
BuildRequires:  pkgconfig(glib-2.0) >= 2.54
BuildRequires:  pkgconfig(gobject-2.0) >= 2.54
BuildRequires:  pkgconfig(gthread-2.0) >= 2.54
BuildRequires:  pkgconfig(gio-2.0) >= 2.54
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(openssl)

%description
libnice is an implementation of the IETF draft Interactive Connectivity
Establishment standard (ICE). ICE is useful for applications that want to
establish peer-to-peer UDP data streams. It automates the process of traversing
NATs and provides security against some attacks. Existing standards that use
ICE include the Session Initiation Protocol (SIP) and Jingle, XMPP extension
for audio/video calls.


%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   glib2-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package doc
Summary:    Documentation for %{name}
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}

%description doc
%{summary}.


%package tests
Summary:    Tests and tests.xml for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   diffutils

%description tests
The %{name}-tests package contains tests and a tests.xml file %{name}.


%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%meson -Dcrypto-library=openssl -Dgupnp=disabled -Dexamples=disabled -Dgtk_doc=disabled -Dintrospection=disabled
%meson_build

%install
%meson_install

find %{buildroot}/opt/tests/%{name}/bin -maxdepth 1 -executable -type f -exec basename {} ';' > tests/libnice-tests.list
sh tests/mktests.sh > %{buildroot}/opt/tests/%{name}/tests.xml

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING COPYING.LGPL COPYING.MPL
%{_bindir}/stunbdc
%{_bindir}/stund
%{_libdir}/gstreamer-1.0/libgstnice.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/nice.pc

%files doc
%defattr(-,root,root,-)
%doc NEWS README

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}

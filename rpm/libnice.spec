Name:       libnice
Summary:    GLib ICE implementation
Version:    0.1.17
Release:    1
License:    LGPLv2.1 and MPLv1.1
URL:        https://libnice.freedesktop.org/
Source0:    %{name}-%{version}.tar.gz
Source1:    mktests.sh
Source2:    INSIGNIFICANT
Source3:    gtk-doc.m4
Patch0:     nemo-tests-install.patch
Patch1:     disable-gtkdoc.patch
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0) >= 2.54
BuildRequires:  pkgconfig(gobject-2.0) >= 2.54
BuildRequires:  pkgconfig(gthread-2.0) >= 2.54
BuildRequires:  pkgconfig(gio-2.0) >= 2.54
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gnutls) >= 2.12.0

%description
libnice is an implementation of the IETF draft Interactive Connectivity
Establishment standard (ICE). ICE is useful for applications that want to
establish peer-to-peer UDP data streams. It automates the process of traversing
NATs and provides security against some attacks. Existing standards that use
ICE include the Session Initiation Protocol (SIP) and Jingle, XMPP extension
for audio/video calls.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   glib2-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package doc
Summary:    Documentation for %{name}
Group:      Documentation
Requires:   %{name} = %{version}-%{release}
Obsoletes:  %{name}-docs

%description doc
%{summary}.


%package tests
Summary:    Tests and tests.xml for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests and a tests.xml file %{name}.


%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%__cp %{SOURCE1} tests/
%__chmod 0755 tests/mktests.sh
%__cp %{SOURCE2} tests/
%__cp %{SOURCE3} m4/

%build
%autogen --disable-gtk-doc

%configure --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
tests/mktests.sh > tests/tests.xml

%install
%make_install
install -m 0644 tests/tests.xml %{buildroot}/opt/tests/%{name}/tests.xml

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

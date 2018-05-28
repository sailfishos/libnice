Name:       libnice
Summary:    GLib ICE implementation
Version:    0.1.14
Release:    1
Group:      System/Libraries
License:    LGPLv2 and MPLv1.1
URL:        http://nice.freedesktop.org/wiki/
Source0:    http://nice.freedesktop.org/releases/%{name}-%{version}.tar.gz
Source1:    mktests.sh
Source2:    INSIGNIFICANT
Source3:    gtk-doc.m4
Patch0:     nemo-tests-install.patch
Patch1:     disable-gtkdoc.patch
Patch2:     0001-fix-test-gstreamer.patch
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0) >= 2.13
BuildRequires:  pkgconfig(gobject-2.0) >= 2.13
BuildRequires:  pkgconfig(gthread-2.0) >= 2.13
BuildRequires:  pkgconfig(gio-2.0) >= 2.13
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gnutls)

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


%if 0%{?with_docs}
%package docs
Summary:    Documentation for development with libnice
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description docs
%{summary}.
%endif


%package tests
Summary:    Tests and tests.xml for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests and a tests.xml file %{name}.


%package examples
Summary:    Examples for libnice
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description examples
%{summary}.


%prep
%setup -q -n %{name}-%{version}/%{name}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%__cp $RPM_SOURCE_DIR/mktests.sh tests/
%__chmod 0755 tests/mktests.sh
%__cp $RPM_SOURCE_DIR/INSIGNIFICANT tests/
%__cp $RPM_SOURCE_DIR/gtk-doc.m4 m4/

%build
%autogen --disable-gtk-doc

%configure --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?jobs:-j%jobs}
tests/mktests.sh > tests/tests.xml

%install
rm -rf %{buildroot}

%make_install
install -m 0644 tests/tests.xml $RPM_BUILD_ROOT/opt/tests/%{name}/tests.xml

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc NEWS README COPYING COPYING.LGPL COPYING.MPL
%{_bindir}/stunbdc
%{_bindir}/stund
%{_libdir}/gstreamer-1.0/libgstnice.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/nice.pc

%if 0%{?with_docs}
%files docs
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/%{name}/
%endif

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}/*

%files examples
%defattr(-,root,root,-)
%{_bindir}/sdp-example
%{_bindir}/simple-example
%{_bindir}/threaded-example

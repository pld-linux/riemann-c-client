#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	Riemann client library
Summary(pl.UTF-8):	Biblioteka kliencka Riemann
Name:		riemann-c-client
Version:	1.10.4
Release:	1
License:	LGPL v3+
Group:		Libraries
#Source0Download: https://github.com/algernon/riemann-c-client/releases
Source0:	https://github.com/algernon/riemann-c-client/archive/%{name}-%{version}.tar.gz
# Source0-md5:	716a0385233b8fbcff13de1a5b4cea10
Patch0:		%{name}-dep.patch
URL:		https://github.com/algernon/riemann-c-client
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	check-devel
BuildRequires:	gnutls-devel >= 2.8
BuildRequires:	json-c-devel >= 0.11
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	protobuf-c-devel
Requires:	json-c >= 0.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a C client library for the Riemann monitoring system,
providing a convenient and simple API, high test coverage and a
copyleft license, along with API and ABI stability.

%description -l pl.UTF-8
Ten pakiet zawiera przeznaczoną dla języka C bibliotekę kliencką
systemu monitorowania Riemann, udostępniającą wygodne i proste API,
mającą duże pokrycie testami oraz licencję typu copyleft, a także
stabilne API i ABI.

%package devel
Summary:	Header files for riemann-client library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki riemann-client
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	protobuf-c-devel

%description devel
Header files for riemann-client library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki riemann-client.

%package static
Summary:	Static riemann-client library
Summary(pl.UTF-8):	Statyczna biblioteka riemann-client
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static riemann-client library.

%description static -l pl.UTF-8
Statyczna biblioteka riemann-client.

%prep
%setup -q -n %{name}-%{name}-%{version}
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libriemann-client.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS.md README.md
%attr(755,root,root) %{_bindir}/riemann-client
%attr(755,root,root) %{_libdir}/libriemann-client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libriemann-client.so.0
%{_mandir}/man1/riemann-client.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libriemann-client.so
%{_includedir}/riemann
%{_pkgconfigdir}/riemann-client.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libriemann-client.a
%endif

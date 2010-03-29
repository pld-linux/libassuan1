#
# Conditional build:
%bcond_without	static_libs	# don't build static library

%define		realname	libassuan
#
Summary:	Assuan - an IPC library for non-persistent servers
Summary(pl.UTF-8):	Assuan - biblioteka IPC dla serwerów nie działających ciągle
Name:		libassuan1
Version:	1.0.5
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/libassuan/%{realname}-%{version}.tar.bz2
# Source0-md5:	c2db0974fcce4401f48f3fa41c4edc5a
Patch0:		%{realname}-shared.patch
Patch1:		%{realname}-info.patch
Patch2:		%{realname}-ac.patch
URL:		http://www.gnupg.org/related_software/libassuan/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	libtool
BuildRequires:	pth-devel >= 1.2.0
BuildRequires:	texinfo
Conflicts:	%{realname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the IPC library used by GnuPG 2, GPGME and a few other
packages. It used to be included with the latter packages but the
authors decided to make your life not too easy and separated it out to
a stand alone library.

%description -l pl.UTF-8
To jest biblioteka komunikacji międzyprocesowej (IPC) używana przez
GnuPG 2, GPGME oraz parę innych pakietów. Była dołączana do tych
pakietów, ale autorzy zdecydowali, żeby już nie ułatwiać tak życia i
wydzielili ją.

%package devel
Summary:	Header files for assuan library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki assuan
Group:		Development/Libraries
Conflicts:	%{realname}-devel
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for assuan library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki assuan.

%package static
Summary:	Static assuan library
Summary(pl.UTF-8):	Statyczna biblioteka assuan
Group:		Development/Libraries
Conflicts:	%{realname}-static
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static assuan library.

%description static -l pl.UTF-8
Statyczna biblioteka assuan.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libassuan.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libassuan.so.0
%attr(755,root,root) %{_libdir}/libassuan-pth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libassuan-pth.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libassuan-config
%attr(755,root,root) %{_libdir}/libassuan.so
%attr(755,root,root) %{_libdir}/libassuan-pth.so
%{_libdir}/libassuan.la
%{_libdir}/libassuan-pth.la
%{_includedir}/assuan.h
%{_aclocaldir}/libassuan.m4
%{_infodir}/assuan.info*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libassuan.a
%{_libdir}/libassuan-pth.a
%endif

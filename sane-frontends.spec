%define name 	sane-frontends
%define version 1.0.14
%define release %mkrel 3
%define beta    %nil
#-beta1

# Enable debug mode
%define debug 0

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary: 	Graphical frontend to SANE
URL:       	http://www.mostang.com/sane/
Source:    	ftp://ftp.mostang.com/pub/sane/sane-%version/%{name}-%{version}%{beta}.tar.bz2
Source1:	sane-frontends16.png
Source2:	sane-frontends32.png
Source3:	sane-frontends48.png
License: 	GPL
Group:		Graphics
BuildRequires:	libgimp-devel >= 2.0
Buildrequires:	libjpeg-devel 
Buildrequires:	libsane-devel >= %{version}
Buildrequires:	libusb-devel
Requires: 	gimp >= 2.0, sane >= %{version}
Buildroot: 	%{_tmppath}/%{name}-%{version}-root

%description
This is the xscanimage program, used to scan images using SANE, either
standalone or as a gimp plugin. Also includes xcam and scanadf.

%prep
%setup -q -n sane-frontends-%{version}%{beta}

%build


%if %debug
export DONT_STRIP=1
CFLAGS="`echo %optflags |sed -e 's/-O3/-g/'`" CXXFLAGS="`echo %optflags |sed -e 's/-O3/-g/'`" \
%endif
%configure
perl -pi -e 's#,-rpath,/usr/lib##' src/Makefile #yves 1.0.5-4mdk
# glibc 2.1 has stpcpy, but sane's configure is apparently unable to detect it.
perl -p -i -e "s|\/\* #undef HAVE_STPCPY \*\/|#define HAVE_STPCPY 1|" include/sane/config.h
%make

%install
rm -rf $RPM_BUILD_ROOT
%if %debug
export DONT_STRIP=1
%endif

%makeinstall

# menu icons
mkdir -p %{buildroot}/{%{_miconsdir},%{_liconsdir},%{_menudir}}
install -m 0644 %SOURCE1 %{buildroot}/%{_miconsdir}/sane-frontends.png
install -m 0644 %SOURCE2 %{buildroot}/%{_iconsdir}/sane-frontends.png
install -m 0644 %SOURCE3 %{buildroot}/%{_liconsdir}/sane-frontends.png

# menu entries
cat > %buildroot/%{_menudir}/sane-frontends << EOF
?package(%{name}): \
command="%{_bindir}/xscanimage" \
icon="sane-frontends.png" \
needs="X11" \
section="Multimedia/Graphics" \
title="XScanImage" \
longtitle="XScanImage is a simple frontend for the SANE scanning system"
?package(%{name}): \
command="%{_bindir}/xcam" \
icon="sane-frontends.png" \
needs="X11" \
section="Multimedia/Graphics" \
title="XCam" \
longtitle="XCam is a SANE-based frontend for webcams"
EOF



%post
%update_menus
if [ -d %{_libdir}/gimp ]; then
  GIMPDIR=`ls -d %{_libdir}/gimp/[012]*`
  [ -z "$GIMPDIR" ] && exit 0
  for i in $GIMPDIR;do
  [ -d $i/plug-ins ] || mkdir -p $i/plug-ins
  %{__ln_s} -f /usr/bin/xscanimage $i/plug-ins/xscanimage
  done
fi

%preun
if [ $1 = 0 ]; then
  if [ -d %{_libdir}/gimp ]; then
    GIMPDIR=`ls -d %{_libdir}/gimp/[012]*`
	[ -z "$GIMPDIR" ] && exit 0
	for i in $GIMPDIR;do
    [ -d $i/plug-ins ] || mkdir -p $i/plug-ins
    %{__rm} -f $i/plug-ins/xscanimage
  	done
  fi
fi

%postun
%update_menus


%clean
rm -R $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc COPYING INSTALL NEWS README AUTHORS
%{_bindir}/*
#config(noreplace) %{_datadir}/sane/sane-style.rc
%{_datadir}/sane/sane-style.rc
%{_mandir}/man1/*
%{_menudir}/*
%{_iconsdir}/*.png
%{_iconsdir}/*/*.png


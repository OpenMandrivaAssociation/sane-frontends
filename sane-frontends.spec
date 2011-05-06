%define name 	sane-frontends
%define version 1.0.14
%define beta    %nil
#-beta1

# Enable debug mode
%define debug 0

Name:           %{name}
Version:        %{version}
Release:        %mkrel 11
Summary: 	Graphical frontend to SANE
URL:       	http://www.mostang.com/sane/
Source:    	ftp://ftp.sane-project.org/pub/sane/sane-frontends-%{version}/%{name}-%{version}%{beta}.tar.bz2
Source1:	sane-frontends16.png
Source2:	sane-frontends32.png
Source3:	sane-frontends48.png
License: 	GPLv2+
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
CFLAGS="`echo %optflags |perl -pi -e 's,-O3,-g,g'`" CXXFLAGS="`echo %optflags |perl -pi -e 's,-O3,-g,g'`" \
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
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 0644 %SOURCE1 %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/sane-frontends.png
install -m 0644 %SOURCE2 %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/sane-frontends.png
install -m 0644 %SOURCE3 %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/sane-frontends.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-xscanimage.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=XScanImage
Comment=A simple frontend for the SANE scanning system
Exec=%{_bindir}/xscanimage
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Graphics;Scanning;
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-xcam.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=XCam
Comment=A SANE-based frontend for webcams
Exec=%{_bindir}/xcam
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;AudioVideo;Video;
EOF

%post
%if %mdkversion < 200900
%update_menus
%endif
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

%if %mdkversion < 200900
%postun
%update_menus
%endif


%clean
rm -R $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc INSTALL NEWS README AUTHORS
%{_bindir}/*
#config(noreplace) %{_datadir}/sane/sane-style.rc
%{_datadir}/sane/sane-style.rc
%{_mandir}/man1/*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png

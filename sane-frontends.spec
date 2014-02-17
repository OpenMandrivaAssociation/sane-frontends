%define name 	sane-frontends
%define version 1.0.14
%define beta    %nil
#-beta1

# Enable debug mode
%define debug 0

Name:           %{name}
Version:        %{version}
Release:        16
Summary: 	Graphical frontend to SANE
URL:       	http://www.mostang.com/sane/
Source:    	ftp://ftp.sane-project.org/pub/sane/sane-frontends-%{version}/%{name}-%{version}%{beta}.tar.bz2
Source1:	sane-frontends16.png
Source2:	sane-frontends32.png
Source3:	sane-frontends48.png
Patch0:		sane-frontends-1.0.14-segfault.patch
License: 	GPLv2+
Group:		Graphics
BuildRequires:	pkgconfig(gimp-2.0)
BuildRequires:	jpeg-devel 
BuildRequires:	pkgconfig(sane-backends)
BuildRequires:  pkgconfig(libusb-1.0)
Requires: 	sane >= %{version}

%description
This is the xscanimage program, used to scan images using SANE, either
standalone or as a gimp plugin. Also includes xcam and scanadf.

%prep
%setup -q -n sane-frontends-%{version}%{beta}
%patch0 -p1

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

mkdir -p %{buildroot}%{_libdir}/gimp/2.0/plug-ins
ln -s %{_bindir}/xscanimage %{buildroot}%{_libdir}/gimp/2.0/plug-ins

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

%files
%defattr(-,root,root,755)
%doc INSTALL NEWS README AUTHORS
%{_bindir}/*
#config(noreplace) %{_datadir}/sane/sane-style.rc
%{_datadir}/sane/sane-style.rc
%{_mandir}/man1/*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_libdir}/gimp/2.0/plug-ins/xscanimage

%changelog
* Fri Sep 14 2012 akdengi <akdengi>
- do not require gimp, this can be used standalone as well
- do not use fragile %%post/preun tricks to install gimp plug-in symlink,
  just create it in %%install

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.14-11mdv2011.0
+ Revision: 669957
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.14-10mdv2011.0
+ Revision: 607508
- rebuild

* Fri Mar 12 2010 Nicolas LÃ©cureuil <nlecureuil@mandriva.com> 1.0.14-9mdv2010.1
+ Revision: 518366
- Remove wrong mimetypes

* Fri Mar 12 2010 Nicolas LÃ©cureuil <nlecureuil@mandriva.com> 1.0.14-8mdv2010.1
+ Revision: 518365
- Remove wrong mimetypes

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.0.14-7mdv2010.0
+ Revision: 426976
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1.0.14-6mdv2009.1
+ Revision: 351530
- rebuild

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 1.0.14-5mdv2009.0
+ Revision: 218438
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.14-5mdv2008.1
+ Revision: 179489
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Aug 30 2007 Adam Williamson <awilliamson@mandriva.org> 1.0.14-4mdv2008.0
+ Revision: 76281
- rebuild for 2008
- don't package COPYING
- xdg menus
- fd.o icons
- use perl rather than sed for CFLAGS substitution (to avoid sed being a build dependency)
- use Fedora license policy
- correct source location


* Tue Jul 04 2006 Till Kamppeter <till@mandriva.com> 1.0.14-3mdv2007.0
- Removed "Requires: gtk+" (Bug 23451).

* Sat Jan 21 2006 Till Kamppeter <till@mandriva.com> 1.0.14-2mdk
- Added menu entries for xscanimage and xcam.
- Introduced %%mkrel.

* Wed Nov 23 2005 Till Kamppeter <till@mandriva.com> 1.0.14-1mdk
- Updated to version 1.0.14.
- Fixed some rpmlint issues.

* Mon Jan 24 2005 Till Kamppeter <till@mandrakesoft.com> 1.0.13-2mdk
- Fixed dependency on GIMP 2.x.

* Tue Nov 09 2004 Till Kamppeter <till@mandrakesoft.com> 1.0.13-1mdk
- Updated to version 1.0.13.

* Mon May 03 2004 Till Kamppeter <till@mandrakesoft.com> 1.0.12-1mdk
- Updated to version 1.0.12.
- GIMP plug-in built for GIMP 2.0 now.

* Fri Aug 22 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 1.0.11-1mdk
- Updated to version 1.0.11

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0.10-2mdk
- rebuild
- rm -rf $RPM_BUILD_ROOT at the beginning of %%install


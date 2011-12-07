%define eclipse_data %{_datadir}/eclipse
# Disable repacking of jars, since it takes forever for all the little jars, 
# and we don't need multilib anyway:
%define __jar_repack %{nil}

%define debug_package %{nil}

Name: eclipse-nls 
Summary: Babel language packs for the Eclipse platform and various plugins
Group: Text Editors/Integrated Development Environments (IDE)
License: EPL
URL: http://babel.eclipse.org/

Version: 3.5.0.v20090620043401
Release: 4%{?dist}
## The source for this package is taken from
# http://download.eclipse.org/technology/babel/babel_language_packs/ *.zip
# and http://download.eclipse.org/technology/babel/update-site/galileo/{artifacts,content}.jar
# or http://build.eclipse.org/technology/babel/test-updates/galileo/{artifacts,content}.jar
# or http://download.eclipse.org/technology/babel/update-site/galileo/site.xml
Source0: BabelLanguagePack-%{version}.tar.bz2

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch: x86_64 %{ix86}
Requires:   eclipse-platform >= 3.4.0-18

%description
Babel language packs include translations for the Eclipse platform and other 
Eclipse-related packages.

%files
%defattr(-,root,root,-)
%dir %{eclipse_data}/dropins/babel
%dir %{eclipse_data}/dropins/babel/eclipse
#% {eclipse_data}/dropins/babel/eclipse/artifacts.jar
#% {eclipse_data}/dropins/babel/eclipse/content.jar
#% dir %{eclipse_data}/dropins/babel/eclipse/features
%dir %{eclipse_data}/dropins/babel/eclipse/plugins


# %1 subpackage id (ie Linux locale id)
# %2 Java locale id (mostly the same as Linux)
# %3 language name
%define lang_meta_pkg() \
%package %1 \
Summary:    Eclipse/Babel language pack for %3 \
Group:      Text Editors/Integrated Development Environments (IDE) \
Requires:   eclipse-nls = %{version}-%{release} \
Obsoletes:  eclipse-sdk-nls-%1 < 3.2.1-4 \
\
%description %1 \
This language pack for %3 contains user-contributed translations of the \
strings in all Eclipse projects. Please see the http://babel.eclipse.org/ \
Babel project web pages for a full how-to-use explanation of these \
translations as well as how you can contribute to \
the translations of this and future versions of Eclipse. \
Note that English text will be displayed if Babel doesn't \
have a translation for a given string. \
\
%files %1 \
%defattr(-,root,root,-) \
#% {eclipse_data}/dropins/babel/eclipse/features/org.eclipse.babel.nls_*_%{2}_%{version} \
%{eclipse_data}/dropins/babel/eclipse/plugins/*.nl_%{2}_%{version}.jar


# Note that no licence %%doc files are listed under %%files.  Upstream 
# does not provide a single distribution archive for eclipse-nls, but 
# rather a collection of 700 zips, one per module/language combination, 
# containing multiple plugin jars.  Each jar does include HTML files 
# with licence information, and these jars are placed in the 
# dropins/babel/eclipse/plugins directory above.

%define spc() %(echo -n ' ')

%lang_meta_pkg ar ar Arabic
%lang_meta_pkg bg bg Bulgarian
%lang_meta_pkg zh zh Chinese%{spc}(Simplified)
%lang_meta_pkg zh_TW zh_TW Chinese%{spc}(Traditional)
%lang_meta_pkg cs cs Czech
%lang_meta_pkg da da Danish
%lang_meta_pkg nl nl Dutch
%lang_meta_pkg en_AU en_AU English%{spc}(Australian)
%lang_meta_pkg et et Estonian
%lang_meta_pkg fi fi Finnish
%lang_meta_pkg fr fr French
%lang_meta_pkg de de German
%lang_meta_pkg el el Greek
# NB 'he' is 'iw' as far as Java is concerned.
# similarly, yi -> ji, id -> in
%lang_meta_pkg he iw Hebrew
%lang_meta_pkg hi hi Hindi
%lang_meta_pkg hu hu Hungarian
%lang_meta_pkg it it Italian
%lang_meta_pkg ja ja Japanese
# tl should be Tagalog.  Klingon has < 1% coverage at present in Babel.  Tagalog is unsupported.
#% lang_meta_pkg tlh tl Klingon
%lang_meta_pkg ko ko Korean
%lang_meta_pkg mn mn Mongolian
%lang_meta_pkg no no Norwegian
%lang_meta_pkg pl pl Polish
%lang_meta_pkg pt pt Portuguese
%lang_meta_pkg pt_BR pt_BR Portuguese%{spc}(Brazilian)
%lang_meta_pkg ro ro Romanian
%lang_meta_pkg ru ru Russian
%lang_meta_pkg es es Spanish
%lang_meta_pkg sv sv Swedish
%lang_meta_pkg tr tr Turkish
%lang_meta_pkg uk uk Ukrainian
%lang_meta_pkg en_AA en_AA Pseudo%{spc}Translations

%prep
# extract langpack zips from tarball
%setup -q -n %{name}
#mkdir -p eclipse/features
mkdir -p eclipse/plugins
# remove unsupported langpacks (currently Klingon)
unsupported="tl"
for locale in $unsupported; do
   rm -f Babel*-${locale}_%{version}.zip
done
# extract remaining zips - to eclipse/{features,plugins}
for f in Babel*.zip; do
   unzip -qq $f
   rm $f
done
#mv artifacts.jar content.jar eclipse
# also ignore site.xml for now
rm -rf eclipse/features

%build
# nothing to build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{eclipse_data}/dropins/babel/
cp -a eclipse $RPM_BUILD_ROOT%{eclipse_data}/dropins/babel/

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jun 10 2010 Sean Flanigan <sflaniga@redhat.com> - 3.5.0.v20090620043401-3
- Marked eclipse-nls as not having debuginfo (#564482)

* Fri Jan 22 2010 Jens Petersen <petersen@redhat.com> - 3.5.0.v20090620043401-3
- only build for x86_64 and i686 like eclipse
  Resolves: #557742

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 3.5.0.v20090620043401-2.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0.v20090620043401-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Sean Flanigan <sflaniga@redhat.com> - 3.5.0.v20090620043401-1
- Updated to Babel's release "0.7"
- Created a new fetch-babel.sh to automate the zip downloads

* Wed May 27 2009 Sean Flanigan <sflaniga@redhat.com> - 3.5.0.v20090423085802-1
- Updated from upstream; added Estonian.
- Fixed names/descriptions for languages with two word names such as "Portuguese (Brazilian)".
- Added Babel metadata files (artifact.jar and content.jar) to make P2 happier (presently disabled)
- Made the base package owner of dropins/babel and subdirectories

* Thu Apr 23 2009 Sean Flanigan <sflaniga@redhat.com> - 3.5.0.v20090417091040-1
- Updated to use Babel's zipped langpacks instead of fetch-babel.sh
- Changed versioning scheme to match changes in upstream versioning
- Updated to latest upstream langpacks for Eclipse 3.5 / Galileo

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-0.6.20080807snap
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 11 2008 Sean Flanigan <sflaniga@redhat.com> - 0.2.0-0.5.20080807snap
- Applied another tidy-up patch from Jens Petersen and added a comment
 about the licence doc files

* Wed Sep 10 2008 Sean Flanigan <sflaniga@redhat.com> - 0.2.0-0.4.20080807snap
- Applied Jens Petersen's suggested patch to remove eclipse_version macro and 
  unnecessary buildroot checks

* Tue Sep 9 2008 Sean Flanigan <sflaniga@redhat.com> - 0.2.0-0.3.20080807snap
- Added eclipse_version macro
- Changed the Obsoletes version to be slightly higher than the last release of 
  eclipse-sdk-nls

* Mon Aug 11 2008 Sean Flanigan <sflaniga@redhat.com> - 0.2.0-0.2.20080807snap
- Fixed version in changelog
- Updated snapshot of Babel translation plugins
- Changed code for Hebrew to he (not iw); changed fetch-babel.sh to compensate
- Renamed eclipse_base macro to eclipse_data

* Fri Jul 25 2008 Sean Flanigan <sflaniga@redhat.com> - 0.2.0-0.1.20080720snap
- Initial rpm package

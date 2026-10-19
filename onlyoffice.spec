%global core_commit ed63e94de814ff1d4ea28cddfaba6939bc9df9ed
%global sdk_commit ae6cf2a039355183c512fc314f7a9bd1a05a6a11
%global apps_commit 332c1905a5361dd4139481827b7ad4f4a9facd85
%global sdkjs_commit 9d2138866d929be32f1d107e8b5bfae36156e097
%global webapps_commit f79972a400c3a696490094961772d1f86fac1b82
%global gumbo_commit aa91b27b02c0c80c482e24348a457ed7c3c088e0
%global katana_commit be6df458d4540eee375c513958dcb862a391cdd1
%global hyphen_commit 482d218738a5affdea467883eb01d5518312ae80

# Version is the 10.0 desktop line. The commits are master of each
# component after "Merge branch release/v10.0.0 into master"
# (2026-10-15), one merge past build tag v10.0.0.176. They are not the
# DesktopEditors v10.0.0 submodule pins; those still point at the May
# 2026 v9.4.0 merges. develop has not moved since May 2026.
# Local abb builds of several packages at once need
# --define "cross_compiling 0". %%cross_compiling races on /tmp/rpm_cc_test.
# ABF is one build per chroot, so the spec does not force that define.

# Directory names under apps/*/main/resources/help/. images and search are
# shared and stay in the main package. sr-Latn becomes the subpackage
# suffix sr_Latn, the same hyphen-to-underscore rule as LibreOffice.
%global help_langs de en es fr it pt ru sr-Latn tr
# converter/templates/<LANG>. Not the same set as the help directories:
# AR, JA and ZH have templates only; tr and sr-Latn have help only.
%global template_langs AR DE EN ES FR IT JA PT RU ZH

Name:		onlyoffice
Version:	10.0.0
Release:	1
Summary:	Office suite for documents, spreadsheets and presentations
Group:		Office
# Program text is AGPL-3.0-only. Non-code assets are CC-BY-SA-4.0.
# agg, xpdf, djvu, jasper, tiff, hyphen, gumbo-parser and katana-parser
# are still compiled from this tree and keep their own licenses.
License:	AGPLv3 and CC-BY-SA-4.0
URL:		https://www.onlyoffice.com/

Source0:	https://github.com/ONLYOFFICE/core/archive/%{core_commit}.tar.gz#/core-%{core_commit}.tar.gz
Source1:	https://github.com/ONLYOFFICE/desktop-sdk/archive/%{sdk_commit}.tar.gz#/desktop-sdk-%{sdk_commit}.tar.gz
Source2:	https://github.com/ONLYOFFICE/desktop-apps/archive/%{apps_commit}.tar.gz#/desktop-apps-%{apps_commit}.tar.gz
Source3:	https://github.com/ONLYOFFICE/sdkjs/archive/%{sdkjs_commit}.tar.gz#/sdkjs-%{sdkjs_commit}.tar.gz
Source4:	https://github.com/ONLYOFFICE/web-apps/archive/%{webapps_commit}.tar.gz#/web-apps-%{webapps_commit}.tar.gz
Source5:	https://github.com/google/gumbo-parser/archive/%{gumbo_commit}.tar.gz#/gumbo-parser-%{gumbo_commit}.tar.gz
Source6:	https://github.com/jasenhuang/katana-parser/archive/%{katana_commit}.tar.gz#/katana-parser-%{katana_commit}.tar.gz
Source7:	https://github.com/hunspell/hyphen/archive/%{hyphen_commit}.tar.gz#/hyphen-%{hyphen_commit}.tar.gz
Source8:	pack-sprites.py
Source9:	pack-startpage.py
# grunt output of pack-startpage.py. npm ci needs a network, so builders
# unpack this instead of running grunt. qmake compiles extras.qrc when
# deploy/noconnect.html is present.
Source10:	loginpage-deploy.tar.gz
# Prints a %package/%description/%files block for one help or templates
# language. Invoked from the bottom of this spec, like
# libreoffice-help-package.
Source11:	onlyoffice-lang-package
# RPM Patch tags are looked up by basename, so a file in patches/core/
# cannot be a Patch tag. ABF packs only declared sources into the SRPM,
# and the git patches directory would be left behind. %%prep unpacks
# this and applies patches/<component>/*.patch with -p1 from inside that
# component. patches/desktop-sdk/DISABLED is not in that glob.
Source12:	onlyoffice-patches.tar.gz

BuildRequires:	make
BuildRequires:	patch
BuildRequires:	m4
BuildRequires:	pkgconf
BuildRequires:	qmake-qt6
BuildRequires:	python
BuildRequires:	hunspell
BuildRequires:	myspell-en
BuildRequires:	myspell-de
BuildRequires:	cef
BuildRequires:	pkgconfig(v8)
BuildRequires:	python%{pyver}dist(pillow)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6PrintSupport)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6Multimedia)
BuildRequires:	pkgconfig(Qt6MultimediaWidgets)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libmng)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(libbrotlidec)
BuildRequires:	pkgconfig(md4c-html)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(icu-i18n)
# Main libheif is shared and its .pc file is just -lheif. x265 and
# libde265 are in restricted, so a main build must not require them.
BuildRequires:	pkgconfig(libheif)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libetonyek-0.1)
BuildRequires:	pkgconfig(libodfgen-0.1)
BuildRequires:	pkgconfig(librevenge-stream-0.0)
BuildRequires:	pkgconfig(librevenge-0.0)
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(cryptopp)
BuildRequires:	pkgconfig(cef)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(x11-xcb)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(cups)
BuildRequires:	cmake(boost_filesystem)
BuildRequires:	cmake(boost_regex)
BuildRequires:	cmake(boost_date_time)

Requires:	cef
Requires:	hicolor-icon-theme
Requires:	hunspell
Requires:	myspell-en
Requires:	myspell-de
Provides:	onlyoffice-desktopeditors = %{EVRD}
Obsoletes:	onlyoffice-desktopeditors <= %{EVRD}
Suggests:	%{name}-help-en = %{EVRD}
Suggests:	%{name}-templates-en = %{EVRD}

%description
OnlyOffice Desktop Editors edits word-processor documents, spreadsheets
and presentations.

Help and document templates are split by language. English is suggested.
Other languages are onlyoffice-help-<lang> and onlyoffice-templates-<lang>.

The Linux build links the system copies of Qt 6, CEF, V8, ICU, libxml2,
FreeType, crypto++, hunspell, minizip-ng and the image codecs. Those
vendored trees are removed after the patches are applied and before
qmake runs, so a bundled header cannot satisfy an include.

%prep
%autosetup -c -n onlyoffice-%{version} -T -N

tar -xf %{SOURCE0}
tar -xf %{SOURCE1}
tar -xf %{SOURCE2}
tar -xf %{SOURCE3}
tar -xf %{SOURCE4}
mv core-%{core_commit} core
mv desktop-sdk-%{sdk_commit} desktop-sdk
mv desktop-apps-%{apps_commit} desktop-apps
mv sdkjs-%{sdkjs_commit} sdkjs
mv web-apps-%{webapps_commit} web-apps

# Patches are written to apply from inside the component. -p1 strips either
# the leading "core/" of a diff -up or the leading "a/" of a diff --git.
tar -xf %{SOURCE12}
for comp in core desktop-sdk desktop-apps sdkjs web-apps; do
	[ -d "$comp" ]
	found=
	for p in patches/$comp/*.patch; do
		[ -f "$p" ] || continue
		found=1
		echo "applying $p"
		patch -d "$comp" -p1 --forward --batch --input="$p"
	done
	if [ -z "$found" ]; then
		echo "no patches for $comp" >&2
		exit 1
	fi
done

mkdir -p core/Common/3dParty/html core/Common/3dParty/hyphen
tar -xf %{SOURCE5}
tar -xf %{SOURCE6}
tar -xf %{SOURCE7}
rm -rf core/Common/3dParty/html/gumbo-parser
rm -rf core/Common/3dParty/html/katana-parser
rm -rf core/Common/3dParty/hyphen/hyphen
mv gumbo-parser-%{gumbo_commit} core/Common/3dParty/html/gumbo-parser
mv katana-parser-%{katana_commit} core/Common/3dParty/html/katana-parser
mv hyphen-%{hyphen_commit} core/Common/3dParty/hyphen/hyphen

# fetch.py replaces the literal string. A sed "isspace(*c)" does not: in
# basic regular expressions the star quantifies the "(".
sed -i -e 's|isspace(\*c)|isspace((unsigned char)*c)|g' \
	core/Common/3dParty/html/gumbo-parser/src/tag.c

katana=core/Common/3dParty/html/katana-parser
sed -i -e 's|static inline bool katana_is_html_space(char c);|static inline bool2 katana_is_html_space(char c);|g' \
	$katana/src/tokenizer.c
sed -i -e 's|inline bool katana_is_html_space(char c)|static inline bool katana_is_html_space(char c)|g' \
	$katana/src/tokenizer.c
sed -i -e 's|static inline bool2 katana_is_html_space(char c);|static inline bool katana_is_html_space(char c);|g' \
	$katana/src/tokenizer.c
sed -i -e 's|katanaget_text(parser->scanner)|/*katanaget_text(parser->scanner)*/\"error\"|g' \
	$katana/src/parser.c
hash=$(printf '\043')
sed -i -e "s|${hash}define KATANA_PARSER_STRING(literal) (KatanaParserString){|${hash}define KATANA_PARSER_STRING(literal) {|g" \
	$katana/src/parser.c

# The bundled headers are included by relative path while the link line is
# already -lcryptopp. Rewrite the includes, then delete the tree.
find core desktop-sdk desktop-apps -type f \
	\( -name '*.h' -o -name '*.hh' -o -name '*.hpp' -o -name '*.c' -o -name '*.cc' -o -name '*.cpp' \) \
	! -path '*/3dParty/cryptopp/*' -print0 \
	| xargs -0 -r sed -i -E 's|#include[[:space:]]*"[^"]*3dParty/cryptopp/([^"]+)"|#include <cryptopp/\1>|'

# Drop vendored copies of libraries the Linux build takes from the system.
# ioapibuf is OnlyOffice's in-memory zip backend and stays. openjpeg's
# src/bin/common/color.c is compiled into opj_bgraframe.cpp. agg, xpdf,
# djvu, jasper, tiff, jbig and the CxImage wrappers are still compiled.
io=$(mktemp -d)
cp -a core/OfficeUtils/src/zlib-1.2.11/contrib/minizip/ioapibuf.c "$io/"
cp -a core/OfficeUtils/src/zlib-1.2.11/contrib/minizip/ioapibuf.h "$io/"
rm -rf core/OfficeUtils/src/zlib-1.2.11
mkdir -p core/OfficeUtils/src/zlib-1.2.11/contrib/minizip
cp -a "$io/ioapibuf.c" "$io/ioapibuf.h" core/OfficeUtils/src/zlib-1.2.11/contrib/minizip/
rm -rf "$io"

oj=core/DesktopEditor/raster/Jp2/openjpeg/openjpeg-2.4.0
keep=$(mktemp -d)
cp -a "$oj/src/bin/common" "$keep/common"
rm -rf "$oj"
mkdir -p "$oj/src/bin"
mv "$keep/common" "$oj/src/bin/common"
rm -rf "$keep"

rm -rf core/DesktopEditor/freetype-2.10.4
rm -rf core/DesktopEditor/freetype-2.5.2
rm -rf core/DesktopEditor/freetype_names/freetype-2.5.3
rm -rf core/DesktopEditor/xml/libxml2
rm -rf core/DesktopEditor/cximage/jpeg
rm -rf core/DesktopEditor/cximage/png
rm -rf core/DesktopEditor/cximage/zlib
rm -rf core/DesktopEditor/cximage/mng
rm -rf core/Common/3dParty/cryptopp
rm -rf core/Common/3dParty/libvlc/build
find core/Common/3dParty -type f \
	\( -name '*.so' -o -name '*.so.*' -o -name '*.dll' -o -name '*.dylib' -o -name '*.a' \) \
	-delete

need() {
	if [ ! -e "$1" ]; then
		echo "missing $1" >&2
		exit 1
	fi
}
gone() {
	if [ -e "$1" ]; then
		echo "still present $1" >&2
		exit 1
	fi
}
need core/OfficeUtils/src/zlib-1.2.11/contrib/minizip/ioapibuf.c
need core/OfficeUtils/src/zlib-1.2.11/contrib/minizip/ioapibuf.h
gone core/OfficeUtils/src/zlib-1.2.11/zlib.h
gone core/OfficeUtils/src/zlib-1.2.11/adler32.c
need "$oj/src/bin/common/color.c"
need core/DesktopEditor/raster/Jp2/openjpeg/opj_apps_config.h
gone "$oj/src/lib"
gone core/Common/3dParty/cryptopp
gone core/DesktopEditor/xml/libxml2
gone core/DesktopEditor/freetype-2.10.4
gone core/DesktopEditor/freetype-2.5.2
gone core/DesktopEditor/freetype_names/freetype-2.5.3
need core/DesktopEditor/freetype_names/FontMaps/FontDictionary.h
gone core/DesktopEditor/cximage/jpeg
gone core/DesktopEditor/cximage/png
gone core/DesktopEditor/cximage/zlib
gone core/DesktopEditor/cximage/mng
need core/DesktopEditor/agg-2.4
need core/PdfFile/lib
need core/DjVuFile/libdjvu
need core/DesktopEditor/cximage/tiff
need core/DesktopEditor/cximage/jasper
need core/Common/3dParty/html/gumbo-parser/src/tag.c
need core/Common/3dParty/html/katana-parser/src/parser.c
need core/Common/3dParty/hyphen/hyphen/hyphen.h
gone core/Common/3dParty/libvlc/build
grep -F -q 'isspace((unsigned char)*c)' core/Common/3dParty/html/gumbo-parser/src/tag.c
grep -F -q 'static inline bool katana_is_html_space(char c)' $katana/src/tokenizer.c
grep -F -q '/*katanaget_text(parser->scanner)*/"error"' $katana/src/parser.c
grep -F -q "KATANA_PARSER_STRING(literal) {" $katana/src/parser.c
if grep -R -n -F '3dParty/cryptopp/' core desktop-sdk desktop-apps \
	--include='*.h' --include='*.hh' --include='*.hpp' \
	--include='*.c' --include='*.cc' --include='*.cpp'
then
	echo "bundled cryptopp include remains" >&2
	exit 1
fi
if find "$oj" core/DesktopEditor/freetype-2.10.4 core/DesktopEditor/xml/libxml2 \
	-name 'openjpeg.h' -o -name 'ft2build.h' -o -name 'libxml.h' 2>/dev/null | grep -q .
then
	echo "bundled public header remains" >&2
	exit 1
fi

# Grunt already ran on a machine with network. This archive is its output.
tar -xf %{SOURCE10} -C desktop-apps/common/loginpage
if [ ! -s desktop-apps/common/loginpage/deploy/noconnect.html ] \
	|| [ ! -s desktop-apps/common/loginpage/deploy/index.html ]
then
	echo "loginpage deploy archive is incomplete" >&2
	exit 1
fi

cp -a %{SOURCE8} pack-sprites.py
cp -a %{SOURCE9} pack-startpage.py

%build
# qmake does not read $CFLAGS. The linux-clang mkspec selects the platform
# and the warning set, including core_linux_64 on every 64-bit target.
# Its release -O2 is replaced with %%{optflags} in qmake() below.
# Projects are sequential because later ones link earlier libraries.
# Each make is parallel.

qmake() {
	# base.pri turns force_debug_info into core_debug, so the rpm flags
	# are added on the release configuration instead. %%{optflags} brings
	# the arch tune, -O3, -g3 and -flto. Drop the mkspec -O2 or it wins.
	# qmake does not read $LDFLAGS. LTO codegen uses the link line, so
	# pass %%{build_ldflags} (the same flags, -Wl,-O2, --no-undefined, -flto).
	qmake-qt6 \
		QMAKE_CFLAGS_RELEASE-=-O2 \
		QMAKE_CXXFLAGS_RELEASE-=-O2 \
		QMAKE_CFLAGS_RELEASE+="%{optflags}" \
		QMAKE_CXXFLAGS_RELEASE+="%{optflags}" \
		QMAKE_LFLAGS+="%{build_ldflags}" \
		"$@"
}

cd core
for i in \
	UnicodeConverter/UnicodeConverter.pro \
	Common/kernel.pro \
	Common/Network/network.pro \
	DesktopEditor/graphics/pro/graphics.pro \
	PdfFile/PdfFile.pro \
	DjVuFile/DjVuFile.pro \
	XpsFile/XpsFile.pro \
	Common/cfcpp/cfcpp.pro \
	OfficeCryptReader/ooxml_crypt/ooxml_crypt.pro \
	DesktopEditor/xmlsec/src/ooxmlsignature.pro \
	OFDFile/OFDFile.pro \
	DocxRenderer/DocxRenderer.pro \
	DesktopEditor/doctrenderer/doctrenderer.pro \
	MsBinaryFile/Projects/VbaFormatLib/Linux/VbaFormatLib.pro \
	OOXML/Projects/Linux/DocxFormatLib/DocxFormatLib.pro \
	OOXML/Projects/Linux/XlsbFormatLib/XlsbFormatLib.pro \
	OOXML/Projects/Linux/PPTXFormatLib/PPTXFormatLib.pro \
	OOXML/Projects/Linux/BinDocument/BinDocument.pro \
	MsBinaryFile/Projects/DocFormatLib/Linux/DocFormatLib.pro \
	MsBinaryFile/Projects/PPTFormatLib/Linux/PPTFormatLib.pro \
	MsBinaryFile/Projects/XlsFormatLib/Linux/XlsFormatLib.pro \
	OdfFile/Projects/Linux/OdfFormatLib.pro \
	RtfFile/Projects/Linux/RtfFormatLib.pro \
	TxtFile/Projects/Linux/TxtXmlFormatLib.pro \
	Fb2File/Fb2File.pro \
	HtmlFile2/HtmlFile2.pro \
	EpubFile/CEpubFile.pro \
	Apple/IWork.pro \
	OdfFile/Reader/Converter/StarMath2OOXML/StarMath2OOXML.pro \
	HwpFile/HWPFile.pro \
	X2tConverter/build/Qt/X2tConverter.pro
do
	echo "=== Building core/$i ==="
	extra=""
	cd "$(dirname "$i")"
	if [ "$(basename "$i")" = graphics.pro ]; then
		hb_raw=$(pkg-config --cflags-only-I harfbuzz)
		extra=$(printf '%s\n' "$hb_raw" | sed -e 's,-I[A-Za-z/]*freetype2,,' | sed -e 's,-I,INCLUDEPATH+=,g')
	fi
	qmake "$(basename "$i")" DEFINES+=_LINUX CONFIG+=core_linux CONFIG+=c++2a $extra
	make %{?_smp_mflags}
	cd - >/dev/null
done
cd ..

cd desktop-sdk/ChromiumBasedEditors/lib
qmake ascdocumentscore.pro CONFIG+=core_linux CONFIG+=c++2a DEFINES+=_LINUX CONFIG+=core_linux QMAKE_CXXFLAGS_RELEASE-=-Werror=format-security
make %{?_smp_mflags}
qmake ascdocumentscore_helper.pro CONFIG+=core_linux CONFIG+=c++2a DEFINES+=_LINUX CONFIG+=core_linux QMAKE_CXXFLAGS_RELEASE-=-Werror=format-security
make %{?_smp_mflags}
cd -
cd desktop-sdk/ChromiumBasedEditors/videoplayerlib
qmake videoplayerlib.pro DEFINES+=_LINUX CONFIG+=core_linux CONFIG+=c++2a
make %{?_smp_mflags}
cd -
cd desktop-sdk/ChromiumBasedEditors/lib/qt_wrapper
qmake qtascdocumentscore.pro DEFINES+=_LINUX CONFIG+=core_linux CONFIG+=c++2a
make %{?_smp_mflags}
cd -

cd desktop-apps/win-linux
glib_raw=$(pkg-config --cflags-only-I glib-2.0)
glib_extra=$(printf '%s\n' "$glib_raw" | sed -e 's,-I,INCLUDEPATH+=,g')
qmake ASCDocumentEditor.pro DEFINES+=_LINUX CONFIG+=core_linux CONFIG+=c++2a $glib_extra
make %{?_smp_mflags}
cd ../..

python sdkjs/build/build.py --desktop

%install
INST=%{buildroot}%{_libdir}/onlyoffice
mkdir -p "$INST/converter" "$INST/fonts" \
	%{buildroot}%{_bindir} \
	%{buildroot}%{_datadir}/applications

editor=$(echo desktop-apps/win-linux/build/*/DesktopEditors)
if [ ! -x "$editor" ]; then
	echo "DesktopEditors was not built" >&2
	find desktop-apps/win-linux/build -name DesktopEditors >&2 || true
	exit 1
fi
plat=$(basename "$(dirname "$editor")")
cp -a "$editor" "$INST/DesktopEditors"
if [ ! -x "core/build/bin/$plat/editors_helper" ]; then
	echo "editors_helper was not built" >&2
	exit 1
fi
cp -a "core/build/bin/$plat/editors_helper" "$INST/editors_helper"
if [ ! -x "core/build/bin/$plat/x2t" ]; then
	echo "x2t was not built" >&2
	exit 1
fi
cp -a "core/build/bin/$plat/x2t" "$INST/converter/x2t"

found=0
for lib in core/build/lib/$plat/lib*.so; do
	[ -f "$lib" ] || continue
	found=1
	cp -a "$lib" "$INST/"
	cp -a "$lib" "$INST/converter/"
done
if [ "$found" != 1 ]; then
	echo "no libraries were built" >&2
	exit 1
fi

cp -a desktop-apps/common/converter/DoctRenderer.config "$INST/converter/DoctRenderer.config"
printf 'package = rpm\n' > "$INST/converter/package.config"
mkdir -p "$INST/converter/empty"
for b in core/Common/empty/*; do
	[ -f "$b" ] || continue
	cp -a "$b" "$INST/converter/empty/"
done
cp -a desktop-apps/common/templates "$INST/converter/templates"

# deploy/index.html is the inlined grunt page. providers sit beside it:
# panelconnect.js sets relpath to "." on Linux.
if [ ! -s desktop-apps/common/loginpage/deploy/index.html ]; then
	echo "missing start page" >&2
	exit 1
fi
cp -a desktop-apps/common/loginpage/deploy/index.html "$INST/index.html"
python pack-startpage.py --templates-only --instdir "$INST"
cp -a desktop-apps/common/loginpage/providers "$INST/providers"

python pack-sprites.py
find web-apps/apps -name app.less -print0 | while IFS= read -r -d '' lessfile; do
	dir=$(dirname "$lessfile")/sprites
	mkdir -p "$dir"
	sed -n 's/.*@import "sprites\/\([^"]*\)".*/\1/p' "$lessfile" | while IFS= read -r name; do
		[ -n "$name" ] || continue
		[ -e "$dir/$name.less" ] || printf '\n' > "$dir/$name.less"
	done
done
mkdir -p "$INST/editors"
cp -a web-apps "$INST/editors/web-apps"
cp -a web-apps/apps/api/documents/index.html.desktop \
	"$INST/editors/web-apps/apps/api/documents/index.html"
if [ -L "$INST/editors/web-apps/apps/api/documents/index.html" ]; then
	echo "documents/index.html is a symlink" >&2
	exit 1
fi

if [ ! -d sdkjs/deploy/sdkjs ]; then
	echo "sdkjs was not deployed" >&2
	exit 1
fi
cp -a sdkjs/deploy/sdkjs "$INST/editors/sdkjs"
rm -rf "$INST/editors/sdkjs/vendor"
cp -a sdkjs/vendor "$INST/editors/sdkjs/vendor"
# Pages under editors/web-apps load develop/sdkjs/<product>/scripts.js.
# sdk-all-min.js loads sdk-all.js itself. Listing both runs font init twice
# and opening a document throws ConvertationOpenError -82.
# common/AllFonts.js is not in the sdkjs checkout. ApplicationFontsWorker
# writes the font map at runtime.
for prod in word cell slide visio; do
	dir="$INST/editors/sdkjs/develop/sdkjs/$prod"
	mkdir -p "$dir"
	cat > "$dir/scripts.js" <<EOF
var sdk_scripts = [
	"../../../../sdkjs/vendor/polyfill.js",
	"../../../../sdkjs/common/AllFonts.js",
	"../../../../sdkjs/${prod}/sdk-all-min.js"
];
EOF
done
if [ ! -f "$INST/editors/sdkjs/vendor/polyfill.js" ]; then
	echo "missing polyfill.js" >&2
	exit 1
fi
if [ ! -f "$INST/editors/sdkjs/word/sdk-all-min.js" ]; then
	echo "missing sdk-all-min.js" >&2
	exit 1
fi

# Grunt inlines the script and the svg. The same file is compiled into
# the binary through extras.qrc when qmake sees it.
if [ ! -s desktop-apps/common/loginpage/deploy/noconnect.html ]; then
	echo "missing noconnect.html" >&2
	exit 1
fi
mkdir -p "$INST/editors/webext"
cp -a desktop-apps/common/loginpage/deploy/noconnect.html \
	"$INST/editors/webext/noconnect.html"

CEF_RES=%{_libdir}/cef/Resources
CEF_REL=%{_libdir}/cef/Release
if [ ! -d "$CEF_RES" ] || [ ! -e "$CEF_REL/libcef.so" ]; then
	echo "distro CEF was not found under %{_libdir}/cef" >&2
	exit 1
fi
for item in "$CEF_RES"/*; do
	[ -e "$item" ] || continue
	ln -s "$item" "$INST/$(basename "$item")"
done
for name in v8_context_snapshot.bin snapshot_blob.bin vk_swiftshader_icd.json libvk_swiftshader.so; do
	if [ ! -e "$CEF_REL/$name" ]; then
		echo "missing $CEF_REL/$name" >&2
		exit 1
	fi
	ln -s "$CEF_REL/$name" "$INST/$name"
done

# Fixed set owned by myspell-en and myspell-de. German dictionaries are
# shipped as <name>_frami and linked under the name the editor asks for.
rm -rf "$INST/dictionaries"
mkdir -p "$INST/dictionaries"
HUN=%{_datadir}/hunspell
for name in en_AU en_CA en_GB en_US en_ZA de_AT de_CH de_DE; do
	aff=$HUN/$name.aff
	dic=$HUN/$name.dic
	if [ ! -e "$aff" ] && [ -e "$HUN/${name}_frami.aff" ]; then
		aff=$HUN/${name}_frami.aff
		dic=$HUN/${name}_frami.dic
	fi
	if [ ! -e "$aff" ] || [ ! -e "$dic" ]; then
		echo "missing dictionary $name" >&2
		exit 1
	fi
	mkdir -p "$INST/dictionaries/$name"
	ln -s "$aff" "$INST/dictionaries/$name/$name.aff"
	ln -s "$dic" "$INST/dictionaries/$name/$name.dic"
done

# Help and template directories are split into per-language subpackages.
# A directory that is not a known language, or a shared help asset
# (images, search), fails the build so it cannot fall into the main package.
for d in "$INST"/editors/web-apps/apps/*/main/resources/help/*/; do
	[ -d "$d" ] || continue
	base=$(basename "$d")
	case " %{help_langs} images search " in
	*" $base "*) ;;
	*)
		echo "unexpected help directory: $base" >&2
		exit 1
		;;
	esac
done
for lang in %{help_langs}; do
	found=
	for d in "$INST"/editors/web-apps/apps/*/main/resources/help/"$lang"; do
		if [ -d "$d" ]; then
			found=1
			break
		fi
	done
	if [ -z "$found" ]; then
		echo "missing help language $lang" >&2
		exit 1
	fi
done
for d in "$INST"/converter/templates/*/; do
	[ -d "$d" ] || continue
	base=$(basename "$d")
	case " %{template_langs} " in
	*" $base "*) ;;
	*)
		echo "unexpected template directory: $base" >&2
		exit 1
		;;
	esac
done
for lang in %{template_langs}; do
	if [ ! -d "$INST/converter/templates/$lang" ]; then
		echo "missing template language $lang" >&2
		exit 1
	fi
done

m4 -I desktop-apps/package/common/linux \
	-D M4_DESKTOPEDITORS_EXEC=onlyoffice \
	-D M4_SCHEME_HANDLER=oo-office \
	desktop-apps/package/common/linux/desktopeditors.desktop.m4 \
	> %{buildroot}%{_datadir}/applications/onlyoffice.desktop
ln -s onlyoffice.desktop \
	%{buildroot}%{_datadir}/applications/onlyoffice-desktopeditors.desktop
for png in desktop-apps/package/common/linux/icons/*.png; do
	size=$(basename "$png" .png)
	icdir=%{buildroot}%{_datadir}/icons/hicolor/$size/apps
	mkdir -p "$icdir"
	cp -a "$png" "$icdir/onlyoffice.png"
	ln -s onlyoffice.png "$icdir/onlyoffice-desktopeditors.png"
done

printf '\043!/bin/sh\n' > %{buildroot}%{_bindir}/onlyoffice
cat >> %{buildroot}%{_bindir}/onlyoffice <<'EOF'
INSTDIR=%{_libdir}/onlyoffice
export LD_LIBRARY_PATH="$INSTDIR:$INSTDIR/converter:%{_libdir}/cef/Release${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
# CEF's Wayland ozone platform does not reparent into the Qt window, so
# each editor opens as its own top-level window and in-app icons do not
# paint. X11 ozone fixes both. Leave a caller-supplied platform alone.
ozone=
for arg in "$@"; do
	case $arg in
	--ozone-platform*) ozone=1 ;;
	esac
done
if [ -n "$ozone" ]; then
	exec "$INSTDIR/DesktopEditors" "$@"
fi
exec "$INSTDIR/DesktopEditors" --ozone-platform=x11 "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/onlyoffice
ln -s onlyoffice %{buildroot}%{_bindir}/onlyoffice-desktopeditors
ln -s onlyoffice %{buildroot}%{_bindir}/desktopeditors

%files
%license core/LICENSE
%{_bindir}/onlyoffice
%{_bindir}/onlyoffice-desktopeditors
%{_bindir}/desktopeditors
%{_libdir}/onlyoffice/
%{expand:%(for l in %{help_langs}; do
echo "%%exclude %%{_libdir}/onlyoffice/editors/web-apps/apps/*/main/resources/help/${l}"
done
for l in %{template_langs}; do
echo "%%exclude %%{_libdir}/onlyoffice/converter/templates/${l}"
done)}
%{_datadir}/applications/onlyoffice.desktop
%{_datadir}/applications/onlyoffice-desktopeditors.desktop
%{_datadir}/icons/hicolor/*/apps/onlyoffice.png
%{_datadir}/icons/hicolor/*/apps/onlyoffice-desktopeditors.png

# Help and template languages. The generator prints %package, %description
# and %files. images/ and search/ under help stay in the main package.
%{expand:%(for l in %{help_langs}; do
/bin/sh %{SOURCE11} help "$l" || exit 1
done
for l in %{template_langs}; do
/bin/sh %{SOURCE11} templates "$l" || exit 1
done)}

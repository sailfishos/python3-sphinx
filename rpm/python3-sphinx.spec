Name:       python3-sphinx
Version:    1.1.3
Release:    8
Summary:    Python documentation generator

# Unless otherwise noted, the license for code is BSD
# sphinx/util/stemmer.py Public Domain
# sphinx/pycode/pgen2 Python
# jquery (MIT or GPLv2)
License:    BSD and Public Domain and Python and (MIT or GPLv2)
URL:        http://sphinx.pocoo.org/
Source0:    %{name}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: python3-devel >= 2.4
BuildRequires: python3-setuptools
BuildRequires: python3-docutils
BuildRequires: python3-jinja2

Requires:      python3-docutils
Requires:      python3-jinja2
Requires:      python3-pygments

%description
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

Sphinx uses reStructuredText as its markup language, and many of its
strengths come from the power and straightforwardness of
reStructuredText and its parsing and translating suite, the Docutils.

Although it is still under constant development, the following
features are already present, work fine and can be seen "in action" in
the Python docs:

    * Output formats: HTML (including Windows HTML Help) and LaTeX,
      for printable PDF versions
    * Extensive cross-references: semantic markup and automatic links
      for functions, classes, glossary terms and similar pieces of
      information
    * Hierarchical structure: easy definition of a document tree, with
      automatic links to siblings, parents and children
    * Automatic indices: general index as well as a module index
    * Code handling: automatic highlighting using the Pygments highlighter
    * Various extensions are available, e.g. for automatic testing of
      snippets and inclusion of appropriately formatted docstrings.

%prep
%autosetup -n %{name}-%{version}/python-sphinx
sed '1d' -i sphinx/pycode/pgen2/token.py

%build
%py3_build

%install
%py3_install

# Move language files to /usr/share;
# patch to support this incorporated in 0.6.6
pushd %{buildroot}%{python3_sitelib}

for lang in $(find sphinx/locale -maxdepth 1 -mindepth 1 -type d -not -path '*/\.*' -exec basename "{}" ";" | tr "\n" " ");
do
  test $lang == __pycache__ && continue
  install -d %{buildroot}%{_datadir}/sphinx/locale/$lang
  install -d %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.js \
     %{buildroot}%{_datadir}/sphinx/locale/$lang/
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.mo \
    %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/
  rm -rf sphinx/locale/$lang
done
popd
%find_lang sphinx

# Language files; Since these are javascript, it's not immediately obvious to
# find_lang that they need to be marked with a language.
(cd %{buildroot} && find . -name 'sphinx.js') | sed -e 's|^.||' | sed -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.js$\):%lang(\2) \1\2\3:' \
  >> sphinx.lang

%files -f sphinx.lang
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/sphinx-*
%{python3_sitelib}/*
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*

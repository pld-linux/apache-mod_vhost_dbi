# $Rev$, $Date: 2005-09-13 09:57:30 $
%define		mod_name	vhost_dbi
%define 	apxs		/usr/sbin/apxs
Summary:	mod_vhost_dbi - dynamic virtual hosting using database to store information
Summary(pl):	mod_vhost_dbi - dynamiczne hosty wirtualne z informacjami trzymanymi w bazie danych
Name:		apache-mod_%{mod_name}
Version:	0.1.0
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.outoforder.cc/downloads/mod_vhost_dbi/mod_%{mod_name}-%{version}.tar.bz2
# Source0-md5:	fd70c654e6b2e78280acb4643207ab68
URL:		http://www.outoforder.cc/projects/apache/mod_vhost_dbi/
BuildRequires:	%{apxs}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	apache-devel >= 2.0.40
BuildRequires:	apache-mod_dbi_pool-devel >= 0.4.0
BuildRequires:	libtool
BuildRequires:	sed
Requires(post,preun):	%{apxs}
Requires:	apache >= 2.0.40
Requires:	apache-mod_dbi_pool >= 0.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
mod_vhost_dbi creates virtual hosts for Apache 2.0 completely
dynamically, without the need to edit your configuration file or
restart Apache if you change a Vhost.

%description -l pl
mod_vhost_dbi tworzy wirtualne hosty dla Apache'a 2.0 w sposób
ca³kowicie dynamiczny, bez potrzeby modyfikowania pliku
konfiguracyjnego czy restartowania Apache'a po zmianie vhosta.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}

sed -i -e 's,test_paths="/usr/lib /usr/local/lib",test_paths="/usr/%{_lib} /usr/lib",g' configure

%configure \
        --with-apxs=%{apxs}
%{__make}
%{__make} -C src make_so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_includedir}/apache}

install src/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*.so

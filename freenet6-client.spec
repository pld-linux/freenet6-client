Summary:	Hexago's TSP Client
Summary(pl.UTF-8):	Klient TSP Hexago
Name:		freenet6-client
Version:	5.1
Release:	1
License:	HPL 1.0
Group:		Applications/System
# Source0: http://www.go6.net/4105/file.asp?file_id=80
Source0:	gw6c-5_1-RELEASE-src.tar.gz
# Source0-md5:	5c5205dc58e82454a5d55a3efb4bf786
Source1:	%{name}.init
Source2:	%{name}.conf
Patch0:		%{name}-pld.patch
URL:		http://www.freenet6.net/
BuildRequires:	libstdc++-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	glibc >= 2.2.1
Requires:	iproute2 >= 2.2.4
Requires:	net-tools >= 1.60
#Requires:	radvd >= 0.6.2
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TSP is a new initiative launched by Hexago, a private company in
Canada involved in IPv6 since 1996, to facilitate a faster deployment
of an IPv6 Internet. The Internet is deployed worldwide over IPv4 so
this project's goal is large scale deployment of IPv6 by using
configured tunnels.

Configured tunneling is a transition method standardized by IETF to
use IPv6 in coexistence with IPv4 by encapsulating IPv6 packets over
IPv4. Any host already connected to Internet with IPv4 which has an
IPv6 stack can establish a link to the Internet IPv6.

Freenet6, developed by Viagenie in 1999/2000, was the first public
tunnel server service and one of the most used in the world to
automatically delegate one single IPv6 address to any host already
connected to an IPv4 network over configured tunnel simply by filling
a web form and running a script. TSP represents another very important
step to accelerate the large scale deployment of IPv6 to everyone on
the net.

Instead of a web interface to request configured tunnels and IPv6
addresses, TSP is a new model based on a client/server approach. A
protocol is used to request a single IPv6 address to a full IPv6
prefix from a client to a tunnel server according to the IPv6 broker
model. The protocol could be integrated directly into the operating
system to provide a service like DHCP but for requesting IPv6
addresses or prefixes over an IPv4 network (Internet).

%description -l pl.UTF-8
TSP to nowa inicjatywa zapoczątkowana przez Hexago - prywatną firmę z
Kanady zaangażowaną w IPv6 od 1996 roku - aby ułatwić szybszy rozwój
Internetu IPv6. Internet jest rozwinięty na całym świecie w oparciu o
IPv4, więc celem tego projektu jest rozwinięcie IPv6 na wielką skalę
poprzez użycie skonfigurowanych tuneli.

Skonfigurowane tunele to metoda przejściowa ustandaryzowana przez IETF
w celu używania IPv6 w koegzystencji z IPv4 poprzez pakowanie pakietów
IPv6 w IPv4. Dowolny host podłączony do Internetu po IPv4 mający stos
IPv6 może łączyć się z Internetem IPv6.

Freenet6 rozwijany przez Viagenie w latach 1999-2000 był pierwszym
publicznym serwerem tuneli i jednym z najbardziej używanych na świecie
do automatycznego delegowania pojedynczych adresów IPv6 do dowolnego
hosta już podłączonego do sieci IPv4 poprzez skonfigurowany tunel po
zwykłym wypełnieniu formularza WWW i uruchomieniu skryptu. TSP
reprezentuje kolejny bardzo ważny krok do przyspieszenia rozwoju IPv6
na szerszą skalę.

Zamiast interfejsu WWW do żądania skonfigurowanych tuneli i adresów
IPv6, TSP jest nowym modelem opartym na komunikacji klient/serwer.
Protokół jest używany do żądania od pojedynczego adresu IPv6 do
pełnego prefiksu IPv6 od klienta do serwera tuneli zgodnie z modelem
brokera IPv6. Protokół może być zintegrowany z systemem operacyjnym,
aby udostępnić usługę typu DHCP, ale do żądania adresów lub prefiksów
IPv6 po sieci IPv4 (Internecie).

%prep
%setup -q -n tspc-advanced
%patch0 -p1

%build
%{__make} all \
	CC="%{__cc} %{rpmcflags} -I\$(INC) -Wall" \
	target=linux \
	installdir=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/gw6c,/etc/rc.d/init.d}

%{__make} install \
	target=linux \
	installdir=$RPM_BUILD_ROOT%{_prefix} \
	install_bin=$RPM_BUILD_ROOT%{_sbindir} \
	install_man=$RPM_BUILD_ROOT%{_mandir} \
	install_template=$RPM_BUILD_ROOT%{_datadir}/gw6c/template

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/freenet6
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/gw6c/gw6c.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add freenet6
if [ -f /var/lock/subsys/freenet6 ]; then
	/etc/rc.d/init.d/freenet6 restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/freenet6 start\" to start freenet6 connection"
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/freenet6 ]; then
		/etc/rc.d/init.d/freenet6 stop 1>&2
	fi
	/sbin/chkconfig --del freenet6
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/gw6c
%dir %{_sysconfdir}/gw6c
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gw6c/gw6c.conf
%attr(754,root,root) /etc/rc.d/init.d/*
%dir %{_datadir}/gw6c
%dir %{_datadir}/gw6c/template
%{_datadir}/gw6c/template/linux.sh
%{_mandir}/man5/*
%{_mandir}/man8/*

Summary:	Hexago's TSP Client
Summary(pl):	Klient TSP Hexago
Name:		freenet6-client
Version:	1.0
Release:	2
License:	HPL 1.0
Group:		Applications/System
Vendor:		Hexago
# http://www.freenet6.net/cgi-bin/download.cgi?fn=freenet6-client-1.0.tgz
Source0:	http://www.kernel.pl/~djurban/pld/%{name}-%{version}.tgz
# Source0-md5:	382450da40cd4334f39e4cad99c583ae
Source1:	freenet6.init
Source2:	tspc.conf
Patch0: 	%{name}-paths.patch
Patch1: 	%{name}-play-nice.patch
URL:		http://www.freenet6.net
Requires:	glibc >= 2.2.1
Requires:	iproute2 >= 2.2.4
Requires:	net-tools >= 1.60
Requires:	radvd >= 0.6.2
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

%description -l pl
TSP to nowa inicjatywa zapocz±tkowana przez Hexago - prywatn± firmê z
Kanady zaanga¿owan± w IPv6 od 1996 roku - aby u³atwiæ szybszy rozwój
Internetu IPv6. Internet jest rozwiniêty na ca³ym ¶wiecie w oparciu o
IPv4, wiêc celem tego projektu jest rozwiniêcie IPv6 na wielk± skalê
poprzez u¿ycie skonfigurowanych tuneli.

Skonfigurowane tunele to metoda przej¶ciowa ustandaryzowana przez IETF
w celu u¿ywania IPv6 w koegzystencji z IPv4 poprzez pakowanie pakietów
IPv6 w IPv4. Dowolny host pod³±czony do Internetu po IPv4 maj±cy stos
IPv6 mo¿e ³±czyæ siê z Internetem IPv6.

Freenet6 rozwijany przez Viagenie w latach 1999-2000 by³ pierwszym
publicznym serwerem tuneli i jednym z najbardziej u¿ywanych na ¶wiecie
do automatycznego delegowania pojedynczych adresów IPv6 do dowolnego
hosta ju¿ pod³±czonego do sieci IPv4 poprzez skonfigurowany tunel po
zwyk³ym wype³nieniu formularza WWW i uruchomieniu skryptu. TSP
reprezentuje kolejny bardzo wa¿ny krok do przyspieszenia rozwoju IPv6
na szersz± skalê.

Zamiast interfejsu WWW do ¿±dania skonfigurowanych tuneli i adresów
IPv6, TSP jest nowym modelem opartym na komunikacji klient/serwer.
Protokó³ jest u¿ywany do ¿±dania od pojedynczego adresu IPv6 do
pe³nego prefiksu IPv6 od klienta do serwera tuneli zgodnie z modelem
brokera IPv6. Protokó³ mo¿e byæ zintegrowany z systemem operacyjnym,
aby udostêpniæ us³ugê typu DHCP, ale do ¿±dania adresów lub prefiksów
IPv6 po sieci IPv4 (Internecie).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} all \
	CC="%{__cc} %{rpmcflags} -I\$(INC) -Wall" \
	target=linux \
	installdir=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/tspc,%{_initrddir}}

%{__make} install \
	target=linux \
	installdir=$RPM_BUILD_ROOT%{_prefix} \
	install_bin=$RPM_BUILD_ROOT%{_sbindir} \
	install_man=$RPM_BUILD_ROOT%{_mandir} \
	install_template=$RPM_BUILD_ROOT%{_datadir}/tspc

install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/freenet6
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/tspc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LEGAL CONTRIB.txt UPDATES
%attr(755,root,root) %{_sbindir}/tspc
%dir %{_sysconfdir}/tspc
%{_sysconfdir}/tspc/tspc.conf
%attr(754,root,root) %{_initrddir}/*
%dir %{_datadir}/tspc
%{_datadir}/tspc/checktunnel.sh
%{_datadir}/tspc/linux.sh
%{_mandir}/man5/*
%{_mandir}/man8/*

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

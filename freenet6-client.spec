Summary:	Hexago's TSP Client
Name:		freenet6-client
Version:	1.0
Release:	1
License:	HPL 1.0
Group:		Applications/System
Vendor:		Hexago
# http://www.freenet6.net/cgi-bin/download.cgi?fn=freenet6-client-1.0.tgz
Source0:	http://www.kernel.pl/~djurban/pld/%{name}-%{version}.tgz
# Source0-md5:	382450da40cd4334f39e4cad99c583ae
Source1:	freenet6.init
Source2:	tspc.conf
Patch0: 	%{name}-paths.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
URL:		http://www.freenet6.net
Requires:	glibc >= 2.2.1
Requires:	radvd >= 0.6.2
Requires:	net-tools >= 1.60
Requires:	iproute2 >= 2.2.4

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
prefix from a clien to a tunnel server according to the IPv6 broker
model. The protocol could be integrated directly into the operating
system to provide a service like DHCP but for requesting IPv6
addresses or prefixes over an IPv4 network (Internet).

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q
%patch0 -p1
%build
CFLAGS="%{rpmcflags}" 
%{__make} all target=linux installdir=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install target=linux installdir=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/tspc/
install -d $RPM_BUILD_ROOT{%{_initrddir},%{_sbindir}}
install -d $RPM_BUILD_ROOT%{_mandir}/man{5,8}/
mv $RPM_BUILD_ROOT/template/linux.sh $RPM_BUILD_ROOT%{_datadir}/tspc/
mv $RPM_BUILD_ROOT/template/checktunnel.sh $RPM_BUILD_ROOT%{_datadir}/tspc/
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/tspc/
cp $RPM_BUILD_ROOT/man/man5/tspc.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/
cp $RPM_BUILD_ROOT/man/man8/tspc.8 $RPM_BUILD_ROOT%{_mandir}/man8/
mv $RPM_BUILD_ROOT/bin/tspc $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LEGAL CONTRIB.txt UPDATES
%{_sysconfdir}/tspc/tspc.conf
%{_datadir}/tspc/*
%attr(755,root,root) %{_sbindir}/tspc
%{_mandir}/man5/*
%{_mandir}/man8/*

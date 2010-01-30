%define rls rc2

Summary:	Daemon utility to control vserver
Name:		openvcpd
Version:	0.5
Release:	%mkrel 0.%{rls}.2
License:	GPLv2+
Group:		Monitoring
URL:		http://openvcp.org/
Source0:	http://files.openvcp.org/%{name}-%{version}%{rls}.tar.gz
Source1:	%{name}.default
Source2:	%{name}.init
Source3:	%{name}.conf
Source4:	%{name}-README.urpmi
Patch1:		openvcpd-0.5-rc2-link.patch
BuildRequires:	iptables-devel >= 1.3.8-1
BuildRequires:	iptables-iptc-devel
BuildRequires:	libxml2-devel
BuildRequires:	python-devel
BuildRequires:	pcap-devel
BuildRequires:	sqlite3-devel
BuildRequires:	util-vserver
BuildRequires:	util-vserver-devel
BuildRequires:	gnutls-devel
BuildRequires:	rsync
BuildRequires:	libtool
Requires:	util-vserver 
Requires:	iptables >= 1.3.8-1
Requires(pre): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OpenVCP is developed for use with Linux in combination with Linux-Vserver.
It provides a web-based interface to manage a whole farm of VServer hosts,
build guests, control the guests, account traffic and much more.

%prep
%setup -q -n %{name}-%{version}%{rls}
%patch1 -p0

cp %{SOURCE1} %{name}.default
cp %{SOURCE2} %{name}.init
cp %{SOURCE3} %{name}.conf
cp %{SOURCE4} %{name}-README.urpmi

%build

%configure2_5x \
    --with-gnutls

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sysconfdir}/default
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}/vservers/backups
install -d %{buildroot}/vservers/images
install -d %{buildroot}/var/run/%{name}
install -d %{buildroot}/var/log/%{name}
install -d %{buildroot}/var/log/ipfm

%makeinstall_std

install -m0755 %{name}.init %{buildroot}%{_initrddir}/%{name}
install -m0644 %{name}.default %{buildroot}%{_sysconfdir}/default/%{name}
install -m0644 %{name}.conf %{buildroot}%{_sysconfdir}/

# install log rotation stuff
cat > %{buildroot}%{_sysconfdir}/logrotate.d/%{name} << EOF
/var/log/openvcp/openvcp.log {
    monthly
    compress
    missingok
    postrotate
	%{_initrddir}/%{name} reload 2> /dev/null || true
    endscript
}
EOF

%post 
%_post_service %{name}

%preun 
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,)
%doc AUTHORS LICENSE README %{name}-README.urpmi
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/default/%{name}
%{_bindir}/*
%{_datadir}/openvcpd
%dir /vservers/backups
%dir /vservers/images
%dir /var/run/%{name}
%dir /var/log/%{name}
%dir /var/log/ipfm

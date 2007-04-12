%define name    openvcpd
%define version 0.2
%define rls rc2

Summary:	Daemon utility to control vserver
Name:		%name
Version:	%version
Release:	%mkrel 2
License:	GPL
Group:		Monitoring
URL:		http://openvcp.org/
Source0:	http://openvcp.org/%name-%version-%{rls}.tar.bz2
Source1:	%{name}.default
Source2:	%{name}.init
Source3:	%{name}.conf
Source4:	%{name}-README.urpmi
Patch0:		openvcpd-0.2rc2-Makefile.patch
BuildRoot:      %_tmppath/%{name}-%{version}-%{release}-buildroot
BuildRequires:	util-vserver util-vserver-devel
Requires:	util-vserver 

Requires(pre): rpm-helper

%description
OpenVCP is developed for use with Linux in combination with Linux-Vserver.
It provides a web-based interface to manage a whole farm of VServer hosts,
build guests, control the guests, account traffic and much more.

%prep
%setup -q -n %name-%version-%{rls}
%patch0 -p0 -b .makefile

%build
%configure2_5x
%make


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_sysconfdir}/default/
mkdir -p %{buildroot}/%{_initrddir}/
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}-%{version}-%{rls}/
%makeinstall_std

cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/default/openvcpd
cp %{SOURCE2} %{buildroot}/%{_initrddir}/openvcpd
cp %{SOURCE3} %{buildroot}/%{_sysconfdir}
cp %{SOURCE4} %{buildroot}/%{_defaultdocdir}/%{name}-%{version}-%{rls}/

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%_post_service openvcpd

%preun 
%_preun_service openvcpd


%files
%defattr(-,root,root,)
%doc AUTHORS LICENSE README
%{_defaultdocdir}/%{name}-%{version}-%{rls}/%{name}-README.urpmi
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/default/%{name}
%{_sysconfdir}/%{name}.conf
%{_initrddir}/openvcpd
%{_bindir}/%{name}
 



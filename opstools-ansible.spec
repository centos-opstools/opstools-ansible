Name:           opstools-ansible
Version:        0.1.0
Release:        2%{?dist}
Summary:        Ansible playbooks for Operational Tools Server installation

License:        ASL 2.0
URL:            https://github.com/centos-opstools
Source0:        https://github.com/centos-opstools/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

Group:          Applications/System
BuildArch:      noarch

BuildRequires:  pandoc
BuildRequires:  python-tox
BuildRequires:  ansible-lint
BuildRequires:  yamllint

Requires:       ansible > 2.2

%description
Ansible playbooks for installing the server side of OpenStack operational tools

%prep
%autosetup -n %{name}-%{version}

%check
tools/validate-playbooks

%build
make

%install
install -d %{buildroot}%{_datadir}/%{name}/group_vars
install -d %{buildroot}%{_datadir}/%{name}/inventory
install -d %{buildroot}%{_datadir}/%{name}/roles
install -p -m 644 ansible.cfg %{buildroot}%{_datadir}/%{name}/ansible.cfg
install -p -m 644 playbook.yml %{buildroot}%{_datadir}/%{name}/playbook.yml
install -p -m 644 playbook-post-install.yml %{buildroot}%{_datadir}/%{name}/playbook-post-install.yml
cp -pr group_vars/* %{buildroot}%{_datadir}/%{name}/group_vars
cp -pr inventory/* %{buildroot}%{_datadir}/%{name}/inventory
cp -pr roles/* %{buildroot}%{_datadir}/%{name}/roles
mkdir -p %{buildroot}%{_sbindir}
install -p -m 755 opstools-server-installation.py %{buildroot}%{_sbindir}/opstools-server-installation

%files
%license LICENSE.txt
%doc README.md
%doc README.html
%{_datadir}/%{name}/
%{_sbindir}/opstools-server-installation



%changelog
* Mon Apr 24 2017 Juan Badia Payno <jbadiapa@redhat.com> - 0.0.2-0.20170424
- Documentation generated automaticaly
- Some playbooks testing

* Tue Oct 11 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 0.0.1-0.20161013gitee599e9
- Initial packaging

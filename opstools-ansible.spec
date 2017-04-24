%global commit0 d736decd3cbc5765b11401736773b42f06c43c09 
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global checkout 20170424git%{shortcommit0}

Name:           opstools-ansible
Version:        0.0.2
Release:        2%{?dist}
Summary:        Ansible playbooks for installing the server side of OpenStack operational tools and its documentation

License:        ASL 2.0
URL:            https://github.com/centos-opstools
Source0:        https://github.com/centos-opstools/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

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
%autosetup -n %{name}-%{commit0}

%check
tools/validate-playbooks

%build 
make

%clean
rm -rf %{buildroot}

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
install -p -m 755 opstools-server-installation.py %{buildroot}%{_sbindir}/opstools-server-installation.py

%files
%defattr(-,root,root)
%license LICENSE.txt
%doc README.md
%doc README.html
%{_datadir}/%{name}/
%{_sbindir}/opstools-server-installation.py



%changelog
* Mon Apr 24 2017 Juan Badia Payno <jbadiapa@redhat.com> - 0.0.2-0.20170424
- Documentation generated automaticaly 
- Some playbooks testing

* Tue Oct 11 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 0.0.1-0.20161013gitee599e9
- Initial packaging

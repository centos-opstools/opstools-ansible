%global with_docs 0
%{!?_licensedir: %global license %%doc}

Name:           opstools-ansible
Version:        0.1.0
Release:        4%{?dist}
Summary:        Ansible playbooks for Operational Tools Server installation

License:        ASL 2.0
URL:            https://github.com/centos-opstools
Source0:        https://github.com/centos-opstools/opstools-ansible/archive/master.tar.gz

Group:          Applications/System
BuildArch:      noarch

Requires:       ansible > 2.2

%description
Ansible playbooks for installing the server side of OpenStack operational tools

%if 0%{?with_docs}
%package docs
Summary:        Ansible playbooks for Operational Tools Server installation

BuildRequires:  python-sphinx

%description docs
Ansible playbooks for installing the server side of OpenStack operational tools

It contains documentation for the opstools-ansible.
%endif

%prep
%autosetup -n %{name}-master
sed -i -e 's/^\#!\/usr\/bin\/env\ python/#\!\/usr\/bin\/python2.7/' opstools-server-installation.py

%build
%if 0%{?with_docs}
# For building docs
%{__python2} setup.py build_sphinx
%endif

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
%doc README.rst
%{_datadir}/%{name}/
%{_sbindir}/opstools-server-installation

%if 0%{?with_docs}
%files docs
%doc docs/build/html
%endif

%changelog
* Wed May 17 2017 Chandan Kumar <chkumar@redhat.com> - 0.1.0-4
- Remove markdown references from doc
- Use github master branch tarball

* Mon May 15 2017 Chandan Kumar <chkumar@redhat.com> - 0.1.0-3
- Added doc subpackage
- README.md docs are moved to RST

* Mon Apr 24 2017 Juan Badia Payno <jbadiapa@redhat.com> - 0.1.0-2
- Documentation generated automaticaly
- Some playbooks testing

* Tue Oct 11 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 0.0.1-0.20161013gitee599e9
- Initial packaging

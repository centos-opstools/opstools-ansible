# opstools-ansible
Ansible playbooks for deploying OpsTools

## Configuration

Create an ansible inventory file in the `inventory/` directory that
defines your hosts and maps them to host groups declared in
`inventory/structure`.  For example:

    server1 ansible_host=192.0.2.7 ansible_user=centos ansible_become=true
    server2 ansible_host=192.0.2.15 ansible_user=centos ansible_become=true

    [am_hosts]
    server1

    [logging_hosts]
    server2

Put any necessary configuration into a ansible variables files.  For
example, I have a file called `config.yml` that contains:

    fluentd_use_ssl: true
    fluentd_shared_key: secret
    fluentd_ca_cert: |
      -----BEGIN CERTIFICATE-----
      ...
      -----END CERTIFICATE-----
    fluentd_private_key:
      -----BEGIN RSA PRIVATE KEY-----
      ...
      -----END RSA PRIVATE KEY-----

Then run the playbook like this:

    ansible-playbook playbook.yml -i inventory -e @config.yml

## Running tests

You can run simple YAML validation tests by running:

    tox

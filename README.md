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

## License

Copyright 2016 Red Hat, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

- http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



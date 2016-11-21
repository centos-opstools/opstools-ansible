<!-- README.md is generated automatically from files and scripts in
the docs/ directory.  If you are editing README.md directly your
changes will be lost. -->

# Overview

The [opstools-ansible][] project is a collection of Ansible roles and
playbooks that will configure an environment that provides centralized
logging and analysis, availability monitoring, and performance
monitoring.

[tripleo]:https://wiki.openstack.org/wiki/TripleO
[opstools-ansible]: https://github.com/larsks/opstools-ansible/

# Requirements

- Ansible 2.2+

# Using opstools-ansible

## Before you begin

Before using the opstools-ansible playbook, you will need to deploy
one or more servers on which you will install the opstools services.
These servers will need to be running either CentOS 7 or RHEL 7 (or a
compatible distribution).

These playbooks will install packages from a number of third-party
repositories.  The opstools-ansible developers are unable to address
problems with the third party packaging (other than via working around
problems in our playbooks).

## Creating an inventory file

Create an Ansible inventory file `inventory/hosts` that defines your
hosts and maps them to host groups declared in `inventory/structure`.
For example:

    server1 ansible_host=192.0.2.7 ansible_user=centos ansible_become=true
    server2 ansible_host=192.0.2.15 ansible_user=centos ansible_become=true

    [am_hosts]
    server1

    [logging_hosts]
    server2

There are two high-level groups that can be used to control service
placement:

- `am_hosts`: The playbooks will install availability monitoring
  software (Sensu, Uchiwa, and support services) on these hosts.

- `logging_hosts`: The playbooks will install the centralized logging
  stack (Elasticsearch, Kibana, Fluentd) on these hosts.

While there are more groups defined in the
`inventory/structure` file, use of those for more granular service
placement is neither tested nor supported at this time.

You can also run post-install playbook after overcloud deployment to finish
server side configuration dependent on the information about the overcloud.
For that you will need to add undercloud host to the inventory. So for example,
after deploying overcloud via tripleo-quickstart tool, you should add something
like following to the inventory file before running the playbook:

undercloud_host ansible_user=stack ansible_host=undercloud ansible_ssh_extra_args='-F "/root/.quickstart/ssh.config.ansible"'

## Create a configuration file

Put any necessary configuration into an Ansible variables file (which
is just a YAML document).  For example, if you wanted to enable
logging via SSL, you would need a configuration file that looked like
this:

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

You don't need a configuration file if you wish to use default
options.

## Run the playbook

Once you have your inventory and configuration in place, you can run
the playbook like this:

    ansible-playbook playbook.yml -e @config.yml

# Roles

The following documentation is automatically extracted from the
`roles` directory in this distribution.

<!-- automatically generated content will be placed here -->
## Fluentd

[Fluentd][] is a log collection tool.  It can collect logs from a
variety of sources, filter them, and send them to a variety of
destinations, including remote Fluentd instances.

We use Fluentd to receive logs from remote Fluentd clients and deliver
them to [Elasticsearch][].

[fluentd]: http://www.fluentd.org/
[elasticsearch]: https://www.elastic.co/products/elasticsearch

### Configuration

- `fluentd_package_name` (default: `"fluentd"`)

    Fluentd package name.

- `fluentd_service_name` (default: `"fluentd"`)

    Fluentd service name.

- `fluentd_config_dir` (default: `"/etc/fluentd"`)

    Path to the Fluentd configuration directory.

- `fluentd_config_file` (default: `"{{ fluentd_config_dir }}/fluent.conf"`)

    Path to the main Fluentd configuration file.

- `fluentd_config_parts_dir` (default: `"{{ fluentd_config_dir }}/config.d"`)

    Path to the directory containing Fluentd configuration snippets.

- `fluentd_owner` (default: `"fluentd"`)

    User that will own Fluentd config files.

- `fluentd_group` (default: `"fluentd"`)

    Group that will own Fluentd config files.

- `fluentd_config_mode` (default: `420`)

    File mode for Fluentd configuration files.

- `fluentd_plugins` (default: `["rubygem-fluent-plugin-secure-forward", "rubygem-fluent-plugin-add"]`)

    A list of Fluentd plugins to install along with Fluentd.

- `fluentd_listen` (default: `false`)

    Set to true if Fluentd should listen for connections from remote
    Fluentd instances.

- `fluentd_use_ssl` (default: `false`)

    Set to true if Fluentd should use SSL.

- `fluentd_shared_key` (default: `null`)

    Shared secret key for SSL connections.

- `fluentd_ca_cert_path` (default: `"{{ fluentd_config_dir }}/ca_cert.pem"`)

    Where to find the Fluentd server certificate authority certificate.

- `fluentd_ca_cert` (default: `null`)

    Content of an x509 certificate that will be used to identify the
    server to clients.

- `fluentd_private_key` (default: `null`)

    The key corresponding to the certificate in `fluentd_ca_cert`.


## Fluentd/Server

This role configures a Fluentd listener that will listen for remote
connections from other Fluentd clients.

### Configuration

- `fluentd_server_plugins` (default: `["rubygem-fluent-plugin-elasticsearch"]`)

    A list of plugins that will be installed on the fluentd server.

- `fluentd_private_key_path` (default: `"{{ fluentd_config_dir }}/ca_key.pem"`)

    Path to the SSL certificate private key.

- `fluentd_server_extraconfig` (default: `{}`)

    Additional fluentd configuration.


## Fluentd/Elasticsearch

This role contains contains configuration to send logs from Fluentd to
an Elasticsearch instance.

### Configuration

- `fluentd_elasticsearch_host` (default: `"localhost"`)

    Address of the Elasticsearch host.

- `fluentd_elasticsearch_port` (default: `9200`)

    Port on which Elasticsearch is accepting connections.

- `fluentd_elasticsearch_index` (default: `"fluentd"`)

    Elasticsearch index name.

- `fluentd_elasticsearch_type` (default: `"fluentd"`)

    Elasticsearch index type.

- `fluentd_elasticsearch_extraconfig` (default: `{}`)

    Additional Fluentd configuration to apply to the Elasticsearch
    output snippet.


## Fluentd/Syslog

This roles installs the necessary configuration to send logs from the
local syslog server to a Fluentd instance.

### Configuration

- `fluentd_syslog_bind_address` (default: `"127.0.0.1"`)

    Address on which to listen for syslog messages.

- `fluentd_syslog_port` (default: `5140`)

    Port on which to listen for syslog messages.

- `fluentd_syslog_tag` (default: `"system.messages"`)

    Fluentd tag to apply to syslog messages.


## Firewall

This role manages the system firewall using either `iptables` or
`firewalld`.

### Configuration

- `firewall_ports` (default: `[]`)

    A list of ports that should be exposed in the system firewall.
    Roles register ports by appending them to this list using the
    `set_fact` module.

- `firewall_manage_rules` (default: `true`)

    Set this to False if you do not want the playbooks to make changes
    to the system firewall.


## Firewall/Commit

This role instantiates the firewall rules that were registered by
other roles during the playbook run.

## Collectd


### Configuration

- `collectd_service_name` (default: `"collectd"`)




## Grafana


### Configuration

- `grafana_package_name` (default: `"grafana"`)




## Sensu/Server

This role is responsible for installing and configuring the Sensu
server.

### Configuration

- `sensu_api_bind` (default: `"0.0.0.0"`)

    Address on which Sensu should listen for connections.

- `sensu_api_port` (default: `4567`)

    Port on which Sensu should listen.

- `sensu_api_server` (default: `"localhost"`)

    Address to which clients should connect to contact the Sensu API.

- `sensu_redis_server` (default: `"127.0.0.1"`)

    Address of the Redis server to which Sensu should connect.

- `sensu_redis_port` (default: `"{{ redis_listen_port }}"`)

    Port on which the Redis server listens.

- `sensu_redis_password` (default: `"{{ redis_password }}"`)

    Password for authenticating to Redis.

- `sensu_enabled_oschecks` (default: `["check-ceilometer_api", "check-ceph_df", "check-ceph_health", "check-cinder_api", "check-cinder_volume", "check-glance_api", "check-keystone_api", "check-neutron_api", "check-nova_api", "check-nova_instance"]`)

    A list of enabled Sensu checks.

- `oscheck_default_username` (default: `"admin"`)

    Username for openstack checks.

- `oscheck_default_password` (default: `"pass"`)

    Password for openstack checks.

- `oscheck_default_project_name` (default: `"admin"`)

    Project name (aka tenant) for openstack checks.

- `oscheck_default_auth_url` (default: `"http://controller:5000/v2.0"`)

    Authentication URL (Keystone server) for openstack checks.

- `oscheck_subscribers_cinder_volume` (default: `"overcloud-cinder-volume"`)

    Region name for openstack checks.


## Sensu/Common

[Sensu][] is a distributed monitoring solution. This role installs the
Sensu package and performs some basic configuration tasks.

[sensu]: http://sensuapp.org/

### Configuration

- `sensu_package_name` (default: `"sensu"`)

    Sensu package name.

- `sensu_server_service_name` (default: `"sensu-server"`)

    Sensu server service name.

- `sensu_api_service_name` (default: `"sensu-api"`)

    Sensu API service name.

- `sensu_client_service_name` (default: `"sensu-client"`)

    Sensu client service name.

- `sensu_config_path` (default: `"/etc/sensu/conf.d"`)

    Path to Sensu configuration directory.

- `sensu_owner` (default: `"sensu"`)

    Owner of Sensu configuration files.

- `sensu_group` (default: `"sensu"`)

    Group of Sensu configuration files.

- `sensu_rabbitmq_server` (default: `"localhost"`)

    Address of RabbitMQ server to which Sensu should connect.

- `sensu_rabbitmq_port` (default: `5672`)

    Port of the RabbitMQ server.

- `sensu_rabbitmq_user` (default: `"sensu"`)

    Authenticate to RabbitMQ server as this user.

- `sensu_rabbitmq_password` (default: `"sensu"`)

    Authenticate to RabbitMQ server with this password.

- `sensu_rabbitmq_vhost` (default: `"/sensu"`)

    RabbitMQ vhost for use by Sensu.


## Opstoolsvhost

This role is responsible for configuring the Apache virtual host that
will host Ops Tools services.

### Configuration

- `opstools_apache_config_file` (default: `"{{ httpd_config_parts_dir }}/opstools.conf"`)

    Path to the Apache configuration file for the Ops Tools virtual host.

- `opstools_apache_config_dir` (default: `"{{ opstools_apache_config_file }}.d"`)

    Path to the directory from which we will read additional
    configuration snipps inside the OpsTools virtual host context.

- `opstools_apache_sslprotocol` (default: `"all -SSLv2"`)

    Apache SSL protocol settings.

- `opstools_apache_sslciphersuite` (default: `"HIGH:MEDIUM:!aNULL:!MD5:!SEED:!IDEA"`)

    Apache SSL cipher suite settings.

- `opstools_apache_sslcert` (default: `"/etc/pki/tls/certs/localhost.crt"`)

    Path to server SSL certificate.

- `opstools_apache_sslkey` (default: `"/etc/pki/tls/private/localhost.key"`)

    Path to SSL private key.

- `opstools_apache_http_port` (default: `80`)

    Port on which to listen for HTTP connections.

- `opstools_apache_https_port` (default: `443`)

    Port on which to listen for HTTPS connections.

- `opstools_default_redirect_file` (default: `"\n{{ opstools_apache_config_dir }}/default_redirect.conf"`)

    Path to configuration file that sets the default redirect for access
    to the root URL (`/`).


## Elasticsearch

[Elasticsearch][] is a search and analytics engine used by Ops Tools
to collect, index, search, and analyze logs.

[elasticsearch]: https://www.elastic.co/products/elasticsearch

### Configuration

- `elasticsearch_package_name` (default: `"elasticsearch"`)

    Name of the Elasticsearch pacakge

- `elasticsearch_service_name` (default: `"elasticsearch"`)

    Name of the Elasticsearch service.

- `elasticsearch_config_dir` (default: `"/etc/elasticsearch"`)

    Path to the Elasticsearch configuration directory.

- `elasticsearch_config_yml` (default: `"{{ elasticsearch_config_dir }}/elasticsearch.yml"`)

    Path to the main Elasticsearch configuration file.

- `elasticsearch_sysconfig` (default: `{}`)

    Values that will be set in /etc/sysconfig/elasticsearch.

- `elasticsearch_sysconfig_path` (default: `"/etc/sysconfig/elasticsearch"`)

    Path to Elasticsearch sysconfig file.

- `elasticsearch_cluster_name` (default: `"elasticsearch"`)

    Elasticsearch cluster name.

- `elasticsearch_port` (default: `9200`)

    Port on which Elasticsearch should listen.

- `elasticsearch_interface` (default: `["127.0.0.1", "::1"]`)

    Addresses on which Elasticsearch should listten.

- `elasticsearch_config` (default: `{"cluster.name": "{{ elasticsearch_cluster_name }}", "network.host": "{{ elasticsearch_interface }}", "http.cors.enabled": true, "http.port": "{{ elasticsearch_port }}", "http.cors.allow-origin": "/.*/"}`)

    Configuration data for Elasticsearch.  The contents of this variable
    will be rendered as YAML in the file referenced by
    `elasticsearch_config_yml`.

- `elasticsearch_extraconfig` (default: `{}`)

    Additional configuration data for Elasticsearch.  Use this if you
    want to add options to `elasticsearch.yml` without replacing the
    defaults in `elasticsearch_config`.

- `java_package_name` (default: `"java"`)

    Name of the package that provides a Java runtime environment.


## Httpd

This role installs the Apache web server and associated modules.

### Configuration

- `httpd_package_name` (default: `"httpd"`)

    Apache package name.

- `httpd_service_name` (default: `"httpd"`)

    Apache service name.

- `httpd_config_dir` (default: `"/etc/httpd"`)

    Path to Apache top-level configuration directory.

- `httpd_config_parts_dir` (default: `"{{ httpd_config_dir }}/conf.d"`)

    Path to directory containing Apache configuration snippets.

- `httpd_owner` (default: `"root"`)

    Owner of Apache configuration files.

- `httpd_group` (default: `"root"`)

    Group of Apache configuration files.

- `httpd_config_mode` (default: `420`)

    Mode of Apache configuration files.

- `httpd_modules` (default: `["mod_ssl"]`)

    Modules that will be installed along with Apache.


## Kibana

[Kibana][] is a web interface for querying an [Elasticsearch][] data
store.

[kibana]: https://www.elastic.co/products/kibana
[elasticsearch]: https://www.elastic.co/products/elasticsearch

### Configuration

- `kibana_path` (default: `"/kibana"`)

    This is the URL path at which clients can access Kibana.

- `kibana_package_name` (default: `"kibana"`)

    The Kibana package name.

- `kibana_service_name` (default: `"kibana"`)

    The Kibana service name.

- `kibana_config_dir` (default: `"/opt/kibana/config"`)

    Path to the Kibana configuration directory.

- `kibana_config_file` (default: `"{{ kibana_config_dir }}/kibana.yml"`)

    Path to the Kibana configuration file.

- `kibana_config_mode` (default: `420`)

    Mode for the Kibana configuration file.

- `kibana_owner` (default: `"kibana"`)

    Owner for the Kibana configuration file.

- `kibana_group` (default: `"kibana"`)

    Group for the Kibana configuration file.

- `kibana_server_bind` (default: `"localhost"`)

    This is address to which Kibana should bind.
    Use "0.0.0.0" to listen on all interfaces; use "localhost" to allow
    access from the local system only.

- `kibana_server_address` (default: `"{{ kibana_server_bind }}"`)

    This is the address to which clients should connect to access Kibana
    (we can't always use kibana_server_bind for that because 0.0.0.0 is
    not an address to which we can connect).

- `kibana_server_port` (default: `5601`)

    The port on which Kibana should listen.

- `kibana_elasticsearch_host` (default: `"localhost"`)

    Address of the Elasticsearch host.

- `kibana_elasticsearch_port` (default: `9200`)

    Port on which Elasticsearch is listening.

- `kibana_server_elasticsearch_url` (default: `"\nhttp://{{ kibana_elasticsearch_host }}:{{ kibana_elasticsearch_port }}"`)

    URL for Kibana to contact Elasticsearch.


## Kibana/Proxy

This role configures the Apache proxy for Kibana.

### Configuration

- `kibana_proxy_dest` (default: `"http://{{ kibana_server_bind }}:{{ kibana_server_port }}"`)

    The URL for the Kibana service.

- `kibana_proxy_htpasswd` (default: `"/etc/httpd/conf/htpasswd-kibana"`)

    Path to the htpasswd file for Kibana.

- `kibana_proxy_user` (default: `"operator"`)

    Initial username for Kibana access to configure in the htpasswd file.

- `kibana_proxy_pass` (default: `"changeme"`)

    Initial password for Kibana access to configure in the htpasswd file.

- `kibana_httpd_conf` (default: `"{{ opstools_apache_config_dir }}/kibana.conf"`)

    Path to the Apache configuration file for Kibana.


## Kibana/Server

This role installs the Kibana web application.  Configuration is taken
from the main `kibana` role.

## Prereqs

This role installs packages and configuration that are required for
the successful operation of the opstools-ansible playbooks.

## Prereqs/Libselinuxpython

This role installs the libselinux-python package (required by Ansible).

### Configuration

- `libselinux_python_package_name` (default: `"libselinux-python"`)

    libselinux-python package name


## Prereqs/Libsemanagepython

This role installs the libsemanage-python package (required by
Ansible).

### Configuration

- `libsemanage_python_package_name` (default: `"libsemanage-python"`)

    libsemanage-python package name


## Rabbitmq

[RabbitMQ][] is a reliable messaging service.  It is used by [Sensu][]
agents to communicate with the Sensu server.

[rabbitmq]: https://www.rabbitmq.com/
[sensu]: https://sensuapp.org/

### Configuration

- `rabbitmq_port` (default: `5672`)

    Port on which RabbitMQ should listen.

- `rabbitmq_server` (default: `"localhost"`)

    Address to which clients should connect to the RabbitMQ service.

- `rabbitmq_interface` (default: `["::"]`)

    Addresses on which RabbitMQ should listen for connections.

- `rabbitmq_package_name` (default: `"rabbitmq-server"`)

    RabbitMQ package name.

- `rabbitmq_service_name` (default: `"rabbitmq-server"`)

    RabbitMQ service name.

- `rabbitmq_default_user` (default: `"guest"`)

    Default RabbitMQ user.

- `rabbitmq_config_file` (default: `"/etc/rabbitmq/rabbitmq.config"`)

    Path to RabbitMQ configuration file.

- `rabbitmq_config_owner` (default: `"rabbitmq"`)

    Owner of RabbitMQ configuration files.

- `rabbitmq_config_group` (default: `"rabbitmq"`)

    Group of RabbitMQ configuration files.

- `rabbitmq_config_mode` (default: `"0644"`)

    Mode of RabbitMQ configuration files.


## Rabbitmq/Server

This role is responsible for installing and starting the RabbitMQ
messaging service.

## Redis

[Redis][] is an in-memory key/value store.  [Sensu][] uses Redis as a
data-store for storing monitoring data (e.g. a client registry,
current check results, current monitoring events, etc).

[redis]: http://redis.io/
[sensu]: http://sensuapp.org/

### Configuration

- `redis_listen_port` (default: `6379`)

    Port on which Redis should listen.

- `redis_password` (default: `"kJadrW$s&5."`)

    Password for accessing the Redis service.


## Redis/Server

This role is responsible for installing and configuring the Redis
service.

### Configuration

- `redis_config_file` (default: `"/etc/redis.conf"`)

    Path to the Redis configuration file.

- `redis_interface` (default: `["127.0.0.1"]`)

    Addresses on which Redis should listen for connections.

- `redis_package_name` (default: `"redis"`)

    Redis package name.

- `redis_service_name` (default: `"redis"`)

    Redis service name.

- `redis_owner` (default: `"redis"`)

    Owner of Redis configuration files.


## Repos

This role is a collection of roles for configuring additional package
repositories.

## Repos/Opstools

This role enables the CentOS OpsTools SIG package repository.

### Configuration

- `opstools_repo_config` (default: `"https://raw.githubusercontent.com/centos-opstools/centos-release-opstools/master/CentOS-OpsTools.repo"`)

    URL to the CentOS OpsTools SIG repository configuration file.
    yamllint disable-line rule:line-length


## Repos/Rdo

This role configures access to the RDO package repository.  This role
is only used on CentOS hosts; it will not configure RDO repositories
on RHEL systems.

### Configuration

- `rdo_release` (default: `"mitaka"`)

    Specify which RDO release to use.


## Rsyslog

This is a utility role for use by other roles that wish to install
rsyslog configuration snippets.  It provides a handler that can be
used to install rsyslogd.  This role will not install or enable
the rsyslog service.

### Configuration

- `rsyslog_config_dir` (default: `"/etc/rsyslog.d"`)

    Path to the directory containing rsyslog configuration snippets.


## Uchiwa

[Uchiwa][] is a web interface to [Sensu][].  This role installs and
configures the Uchiwa service.

[sensu]: http://sensuapp.org/
[uchiwa]: https://uchiwa.io/

### Configuration

- `uchiwa_package_name` (default: `"uchiwa"`)

    Uchiwa package name.

- `uchiwa_service_name` (default: `"uchiwa"`)

    Uchiwa service name.

- `uchiwa_bind` (default: `"127.0.0.1"`)

    Address on which Uchiwa should listen for connections.

- `uchiwa_server_address` (default: `"localhost"`)

    Address to which clients should connect to Uchiwa.

- `uchiwa_port` (default: `3000`)

    Port on which Uchiwa should listen.

- `uchiwa_refresh` (default: `5`)

    How often Uchiwa should refresh results.

- `uchiwa_file_path` (default: `"/etc/sensu/uchiwa.json"`)

    Path to Uchiwa configuration file.

- `sensu_datacenters` (default: `[{"host": "{{ sensu_api_server }}", "name": "{{ uchiwa_sensu_api_server_name }}", "port": "{{ sensu_api_port }}"}]`)

    List of Sensu datacenters to which Uchiwa should connect.


## Uchiwa/Proxy

This role configures the Apache proxy for Uchiwa.

### Configuration

- `uchiwa_proxy_dest` (default: `"http://{{ uchiwa_bind }}:{{ uchiwa_port }}"`)

    URL for backend Uchiwa service.

- `uchiwa_proxy_htpasswd` (default: `"/etc/httpd/conf/htpasswd-uchiwa"`)

    Path to htpasswd file for controlling access to Uchiwa.

- `uchiwa_proxy_user` (default: `"operator"`)

    User to create in htpasswd file.

- `uchiwa_proxy_pass` (default: `"changeme"`)

    Password for user in htpasswd file.

- `uchiwa_httpd_conf` (default: `"{{ opstools_apache_config_dir }}/uchiwa.conf"`)

    Path to the Apache configuration snippet for the Uchiwa proxy.

- `uchiwa_path` (default: `"/uchiwa"`)

    URL path at which to host Uchiwa.


## Chrony

Installs and configures an NTP client ([Chrony][]) to ensure that the
server keeps correct time.  Clock skew between the server and clients
can cause unexpected behaviors.

[chrony]: https://chrony.tuxfamily.org/

### Configuration

- `chrony_package_name` (default: `"chrony"`)

    The name of the Chrony package.

- `chrony_service_name` (default: `"chronyd"`)

    The name of the Chrony service.

- `chrony_config_file` (default: `"/etc/chrony.conf"`)

    Path to the Chrony configuration file.

- `chrony_driftfile` (default: `"/var/lib/chrony/drift"`)

    Path to the Chrony driftfile.

- `chrony_logdir` (default: `"/var/log/chrony"`)

    Path to the Chrony log directory.

- `chrony_pools` (default: `["pool.ntp.org iburst"]`)

    A list of pools to use for synchronziation.  Each item is provided'
    directly to the `pool` command.

- `chrony_default_config` (default: `["makestep 1.0 3", "rtcsync"]`)

    A list of configuration items that will be included verbatim in the
    Chrony configuration.


# Integration with TripleO

The [TripleO][] installer for OpenStack includes support for Fluentd
and Sensu clients.  See [tripleo-integration.md][] in the `docs/`
subdirectory of this repository.

[tripleo-integration.md]: docs/tripleo-integration.md

# Contributing

If you encounter problems with or have suggestions about
opstools-ansible, open an issue on our [Github issue tracker][].

If you would like to contribute code, documentation, or other changes
to the project, please read the [docs/developers.md][] document located in
the `docs/` subdirectory of this repository.

[github issue tracker]: https://github.com/centos-opstools/opstools-ansible/issues
[developers.md]: docs/developers.md

# License

Copyright 2016 [Red Hat, Inc.][redhat]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

- http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

[redhat]: http://www.redhat.com/

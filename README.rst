Overview
--------

The `opstools-ansible <https://github.com/larsks/opstools-ansible/>`__
project is a collection of Ansible roles and playbooks that will
configure an environment that provides centralized logging and analysis,
availability monitoring, and performance monitoring.

Using opstools-ansible
----------------------

Before you begin
++++++++++++++++

Before using the opstools-ansible playbook, you will need to deploy one
or more servers on which you will install the opstools services. These
servers will need to be running either CentOS 7 or RHEL 7 (or a
compatible distribution).

These playbooks will install packages from a number of third-party
repositories. The opstools-ansible developers are unable to address
problems with the third party packaging (other than via working around
problems in our playbooks).

Creating an inventory file
++++++++++++++++++++++++++

Create an Ansible inventory file ``inventory/hosts`` that defines your
hosts and maps them to host groups declared in ``inventory/structure``.
For example:

::

    server1 ansible_host=192.0.2.7 ansible_user=centos ansible_become=true
    server2 ansible_host=192.0.2.15 ansible_user=centos ansible_become=true

    [am_hosts]
    server1

    [pm_hosts]
    server2

    [logging_hosts]
    server2

There are three high-level groups that can be used to control service
placement:

-  ``am_hosts``: The playbooks will install availability monitoring
   software (Sensu, Uchiwa, and support services) on these hosts.

 - ``pm_hosts``: The playbooks will install performance monitoring
   software (Gnocchi or graphite)

-  ``logging_hosts``: The playbooks will install the centralized logging
   stack (Elasticsearch, Kibana, Fluentd) on these hosts.

While there are more groups defined in the ``inventory/structure`` file,
use of those for more granular service placement is neither tested nor
supported at this time.

You can also run post-install playbook after overcloud deployment to
finish server side configuration dependent on the information about the
overcloud. For that you will need to add undercloud host to the
inventory. So for example, after deploying overcloud via
tripleo-quickstart tool, you should add something like following to the
inventory file before running the playbook:

undercloud\_host ansible\_user=stack ansible\_host=undercloud
ansible\_ssh\_extra\_args='-F "/root/.quickstart/ssh.config.ansible"'

Create a configuration file
+++++++++++++++++++++++++++

Put any necessary configuration into an Ansible variables file (which is
just a YAML document). For example, if you wanted to enable logging via
SSL, you would need a configuration file that looked like this:

::

    fluentd_use_ssl: true
    fluentd_shared_key: secret
    fluentd_ca_cert: |
      -----BEGIN CERTIFICATE-----
      ...
      -----END CERTIFICATE-----
    fluentd_private_key: |
      -----BEGIN RSA PRIVATE KEY-----
      ...
      -----END RSA PRIVATE KEY-----

You can also influence the data storage being used for performance metrics.
It can be either gnocchi or graphite, which should work in most cases.
For more details, please visit group_vars/all.yml.

You don't need a configuration file if you wish to use default options.

Run the playbook
++++++++++++++++

Once you have your inventory and configuration in place, you can run the
playbook like this:

::

    ansible-playbook playbook.yml -e @config.yml

Roles
-----

The following documentation is automatically extracted from the
``roles`` directory in this distribution.

.. raw:: html

   <!-- automatically generated content will be placed here -->

Uchiwa
------

`Uchiwa <https://uchiwa.io/>`__ is a web interface to
`Sensu <http://sensuapp.org/>`__. This role installs and configures the
Uchiwa service.

Configuration
+++++++++++++

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



Actions defined on the role
+++++++++++++++++++++++++++

- Install uchiwa
- Configure uchiwa
- Add uchiwa user to additional groups
- Ensure uchiwa is started and enabled at boot
- Create appropriate firewall rules



Uchiwa/Proxy
------------

This role configures the Apache proxy for Uchiwa.

Actions defined on the role
+++++++++++++++++++++++++++

- Install uchiwa configuration for Apache
- Create uchiwa htpasswd file
- Secure uchiwa htpasswd file
- Configure default redirect


Configuration
+++++++++++++

- `uchiwa_proxy_dest` (default: `"http://{{ uchiwa_bind }}:{{ uchiwa_port }}"`)

    URL for backend Uchiwa service.

- `uchiwa_proxy_htpasswd` (default: `"/etc/httpd/conf/htpasswd-uchiwa"`)

    Path to htpasswd file for controlling access to Uchiwa.

- `uchiwa_httpd_conf` (default: `"{{ opstools_apache_config_dir }}/uchiwa.conf"`)

    Path to the Apache configuration snippet for the Uchiwa proxy.

- `uchiwa_path` (default: `"/uchiwa"`)

    URL path at which to host Uchiwa.

- `uchiwa_credentials` (default: `["username": "operator", "password": "changeme"`])

    List of Users and Passwords to create in htpasswd file


Sensu
-----

This role is responsible for installing and configuring the Sensu.

Configuration
+++++++++++++

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

- `sensu_log_path` (default: `"/var/log/sensu"`)

    Path to Sensu log directory.

- `sensu_runtime_path` (default: `"/var/run/sensu"`)

    Path to Sensu runtime directory.

- `sensu_owner` (default: `"sensu"`)

    Owner of Sensu configuration files.

- `sensu_group` (default: `"sensu"`)

    Group of Sensu configuration files.

- `sensu_rabbitmq_server` (default: `"localhost"`)

    Address of RabbitMQ server to which Sensu should connect.

- `sensu_rabbitmq_port` (default: `5672`)

    Port of the RabbitMQ server.

- `sensu_rabbitmq_ssl_port` (default: `5671`)

    Port of the RabbitMQ server for SSL communication.

- `sensu_rabbitmq_user` (default: `"sensu"`)

    Authenticate to RabbitMQ server as this user.

- `sensu_rabbitmq_password` (default: `"sensu"`)

    Authenticate to RabbitMQ server with this password.

- `sensu_rabbitmq_vhost` (default: `"/sensu"`)

    RabbitMQ vhost for use by Sensu.

- `sensu_api_bind` (default: `"0.0.0.0"`)

    Address on which Sensu should listen for connections.

- `sensu_api_port` (default: `4567`)

    Port on which Sensu API should listen.

- `sensu_api_server` (default: `"localhost"`)

    Address to which clients should connect to contact the Sensu API.

- `sensu_redis_server` (default: `"127.0.0.1"`)

    Address of the Redis server to which Sensu should connect.

- `sensu_redis_port` (default: `"{{ redis_listen_port }}"`)

    Port on which the Redis server listens.

- `sensu_redis_password` (default: `"{{ redis_password }}"`)

    Password for authenticating to Redis.

- `sensu_client_subscription` (default: `"monitoring-node"`)

    Subscription string for monitoring host

- `sensu_client_bind` (default: `"127.0.0.1"`)

    Address on which Sensu client should listen on monitoring host.

- `sensu_client_port` (default: `3030`)

    Port on which Sensu client should listen on monitoring host.

- `sensu_client_name` (default: `"{{ ansible_fqdn }}"`)

    Name for client service displayed in Uchiwa

- `sensu_client_address` (default: `"{{ ansible_default_ipv4.address }}"`)

    Address for client service displayed in Uchiwa

- `sensu_manage_checks` (default: `true`)

    Whether oschecks and default checks should be installed

- `sensu_overcloud_checks` (default: `[{"name": "aodh-evaluator", "subscribers": ["overcloud-ceilometer-aodh-evaluator"]}, {"name": "aodh-listener", "subscribers": ["overcloud-ceilometer-aodh-listener"]}, {"name": "aodh-notifier", "subscribers": ["overcloud-ceilometer-aodh-notifier"]}, {"name": "ceilometer-central", "subscribers": ["overcloud-ceilometer-agent-central"]}, {"name": "ceilometer-collector"}, {"name": "ceilometer-compute"}, {"name": "ceilometer-compute", "subscribers": ["overcloud-ceilometer-agent-compute"]}, {"name": "ceilometer-notification", "subscribers": ["overcloud-ceilometer-agent-notification"]}, {"name": "ceilometer-polling"}, {"name": "ceph-df"}, {"name": "ceph-health"}, {"name": "cinder-api"}, {"name": "cinder-scheduler"}, {"name": "cinder-volume"}, {"name": "glance-api"}, {"name": "glance-registry"}, {"name": "haproxy", "service": "haproxy"}, {"name": "heat-api"}, {"name": "heat-api-cfn"}, {"name": "heat-api-cloudwatch"}, {"name": "heat-engine"}, {"name": "memcached", "service": "memcached"}, {"name": "neutron-api", "service": "neutron-server"}, {"name": "neutron-l3-agent", "service": "neutron-l3-agent"}, {"service": "neutron-metadata-agent", "name": "neutron-metadata-agent", "subscribers": ["overcloud-neutron-metadata"]}, {"name": "neutron-ovs-agent", "service": "neutron-openvswitch-agent"}, {"name": "nova-api"}, {"name": "nova-compute"}, {"name": "nova-conductor"}, {"name": "nova-consoleauth"}, {"name": "nova-libvirt", "service": "libvirtd"}, {"name": "nova-novncproxy", "subscribers": ["overcloud-nova-vncproxy"]}, {"name": "nova-scheduler"}, {"name": "pacemaker", "service": "pacemaker"}, {"name": "swift-proxy"}]`)

    A list of Sensu checks that will run on the overcloud hosts. The
    only required key for each item is `name`. The systemd `service`
    used in `systemctl` checks defaults to `openstack-<name>`, and the
    `subscribers` key defaults to `[ "overcloud-<name>" ]`.

    The following checks are disabled because the corresponding services
    are run as WSGI applications under Apache.  This means that we don't
    have a good client-side healthcheck until we make changes either to
    sensu packaging or our tripleo integration.

    .. code-block:: yaml

        - name: ceilometer-api
        - name: keystone-api
          subscribers:
            - overcloud-keystone
            - overcloud-kestone
        - name: aodh-api
          subscribers:
            - overcloud-ceilometer-aodh-api

- `sensu_overcloud_checks_pcs`

    A list of Sensu checks that will run on the overcloud hosts. Used
    for pcs resources.

- `sensu_remote_checks` (default: `[]`)

    A list of sensu checks that will run on an opstools server

- `oscheck_default_username` (default: `"admin"`)

    Username for openstack checks.

- `oscheck_default_password` (default: `"pass"`)

    Password for openstack checks.

- `oscheck_default_project_name` (default: `"admin"`)

    Project name (aka tenant) for openstack checks.

- `oscheck_default_auth_url` (default: `"http://controller:5000/v2.0"`)

    Authentication URL (Keystone server) for openstack checks.

- `oscheck_default_region_name` (default: `"RegionOne"`)

    Region name for openstack checks.



Sensu/Server
------------

This role is responsible for installing and configuring the Sensu
server.

Actions defined on the role
+++++++++++++++++++++++++++

- Configure sensu
- Configure sensu checks
- Create sensu vhost on rabbitmq
- Configure rabbitmq permissions
- Ensure correct ownership on directories
- Ensure sensu is started and enabled at boot
- Create appropriate firewall rules



Actions defined on the role
+++++++++++++++++++++++++++

- Fetch overcloud node address
- Set facts from result data
- Update client configuration on monitoring host



Sensu/Common
------------

`Sensu <http://sensuapp.org/>`__ is a distributed monitoring solution.
This role installs the Sensu package and performs some basic
configuration tasks.

Actions defined on the role
+++++++++++++++++++++++++++

- Enable Sensu repository
- Ensure repoquery command is available
- Check for obsolete sensu package
- Remove obsolete sensu package
- Install sensu
- Configure rabbitmq on sensu


Configuration
+++++++++++++

- `sensu_rabbitmq_with_ssl` (default: `false`)

    Enable SSL connections

- `sensu_rabbitmq_ssl_cert` (default: `null`)

    Content of SSL certificate to be created on Sensu client node.

- `sensu_rabbitmq_ssl_key` (default: `null`)

    Content of SSL key to be created on Sensu client node.

- `sensu_rabbitmq_ssl_certs_path` (default: `"/etc/sensu/ssl"`)

    Path to where certificates/key should be created on Sensu client node.



Sensu/Client
------------

This role is responsible for installing and configuring the Sensu
client.

Actions defined on the role
+++++++++++++++++++++++++++

- Configure sensu client
- Ensure correct ownership on directories
- Ensure sensu-client is started and enabled at boot
- Install oschecks package



Rsyslog
-------

This is a utility role for use by other roles that wish to install
rsyslog configuration snippets. It provides a handler that can be used
to install rsyslogd. This role will not install or enable the rsyslog
service.

Configuration
+++++++++++++

- `rsyslog_config_dir` (default: `"/etc/rsyslog.d"`)

    Path to the directory containing rsyslog configuration snippets.



Repos
-----

This role is a collection of roles for configuring additional package
repositories.


Repos/Rdo
---------

This role configures access to the RDO package repository. This role is
only used on CentOS hosts; it will not configure RDO repositories on
RHEL systems.

Actions defined on the role
+++++++++++++++++++++++++++

- Install rdo repository configuration


Configuration
+++++++++++++

- `rdo_release` (default: `"queens"`)

    Specify which RDO release to use.



Repos/Opstools
--------------

This role enables the CentOS OpsTools SIG package repository.

Actions defined on the role
+++++++++++++++++++++++++++

- Install centos-release-opstools
- Install centos-opstools repository (if needed)


Configuration
+++++++++++++

- `opstools_repo_config` (default: `"https://raw.githubusercontent.com/centos-opstools/centos-release-opstools/master/CentOS-OpsTools.repo"`)

    URL to the CentOS OpsTools SIG repository configuration file.
    yamllint disable-line rule:line-length



Redis
-----

`Redis <http://redis.io/>`__ is an in-memory key/value store.
`Sensu <http://sensuapp.org/>`__ uses Redis as a data-store for storing
monitoring data (e.g. a client registry, current check results, current
monitoring events, etc).

Configuration
+++++++++++++

- `redis_listen_port` (default: `6379`)

    Port on which Redis should listen.

- `redis_password` (default: `"kJadrW$s&5."`)

    Password for accessing the Redis service.



Redis/Server
------------

This role is responsible for installing and configuring the Redis
service.

Actions defined on the role
+++++++++++++++++++++++++++

- Install redis
- Set listen port at redis config
- Add bind interface at the redis config
- Ensure protected mode is enabled
- Set password
- Ensure redis is started and enabled at boot
- Create appropriate firewall rules


Configuration
+++++++++++++

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



Rabbitmq
--------

`RabbitMQ <https://www.rabbitmq.com/>`__ is a reliable messaging
service. It is used by `Sensu <https://sensuapp.org/>`__ agents to
communicate with the Sensu server.

Configuration
+++++++++++++

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

- `rabbitmq_use_ssl` (default: `false`)

    Enable SSL connections

- `rabbitmq_ssl_cacert` (default: `null`)

    Content of CA certificate to be created on RabbitMQ server node.

- `rabbitmq_ssl_cert` (default: `null`)

    Content of server certificate to be created on RabbitMQ server node.

- `rabbitmq_ssl_key` (default: `null`)

    Content of server key to be created on RabbitMQ server node.

- `rabbitmq_ssl_certs_path` (default: `"/etc/rabbitmq/ssl"`)

    Path to where certificates/key should be created on server node.

- `rabbitmq_ssl_port` (default: `5671`)

    Port on which RabbitMQ should listen on for SSL connections.

- `rabbitmq_ssl_fail_no_cert` (default: `"false"`)

    Fail for clients without a certificate to send to the RabbitMQ server.

- `rabbitmq_ssl_verify` (default: `"verify_peer"`)

    Valid values are:
        verify_peer - ensure a chain of trust is established when the client sends
                      a certificate
        verify_none - no certificate exchange takes place from the client
                      to the server



Rabbitmq/Server
---------------

This role is responsible for installing and starting the RabbitMQ
messaging service.

Actions defined on the role
+++++++++++++++++++++++++++

- Install rabbitmq-server rpm
- Generate rabbitmq configuration
- Add plugin to manage rabbitmq
- Start the rabbitmq service
- Delete guest user on rabbitmq
- Create appropriate firewall rules



Prereqs
-------

This role installs packages and configuration that are required for the
successful operation of the opstools-ansible playbooks.


Prereqs/Pythonnetaddr
---------------------

This role installs the python-netaddr package (required by Ansible).

Actions defined on the role
+++++++++++++++++++++++++++

- Install python-netaddr


Configuration
+++++++++++++

- `python_netaddr_package_name` (default: `"python-netaddr"`)





Prereqs/Libsemanagepython
-------------------------

This role installs the libsemanage-python package (required by Ansible).

Actions defined on the role
+++++++++++++++++++++++++++

- Install libsemanage python


Configuration
+++++++++++++

- `libsemanage_python_package_name` (default: `"libsemanage-python"`)

    libsemanage-python package name



Prereqs/Libselinuxpython
------------------------

This role installs the libselinux-python package (required by Ansible).

Actions defined on the role
+++++++++++++++++++++++++++

- Install libselinux python


Configuration
+++++++++++++

- `libselinux_python_package_name` (default: `"libselinux-python"`)

    libselinux-python package name



Configuration
+++++++++++++

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

- `opstools_apache_force_https` (default: `true`)

    Force all http request to https



Opstoolsvhost
-------------

This role is responsible for configuring the Apache virtual host that
will host Ops Tools services.

Actions defined on the role
+++++++++++++++++++++++++++

- Ensure opstools httpd config directory exists
- Install opstools httpd config file



Kibana
------

`Kibana <https://www.elastic.co/products/kibana>`__ is a web interface
for querying an
`Elasticsearch <https://www.elastic.co/products/elasticsearch>`__ data
store.

Configuration
+++++++++++++

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



Kibana/Server
-------------

This role installs the Kibana web application. Configuration is taken
from the main ``kibana`` role.

Actions defined on the role
+++++++++++++++++++++++++++

- Enable kibana repository
- Install kibana package
- Ensure kibana configuration directory exists
- Create kibana configuration file
- Enable kibana service



Kibana/Proxy
------------

This role configures the Apache proxy for Kibana.

Actions defined on the role
+++++++++++++++++++++++++++

- Install kibana configuration for Apache
- Create kibana htpasswd file
- Secure htpasswd file
- Configure default redirect
- Create appropriate firewall rules


Configuration
+++++++++++++

- `kibana_proxy_dest` (default: `"http://{{ kibana_server_bind }}:{{ kibana_server_port }}"`)

    The URL for the Kibana service.

- `kibana_proxy_htpasswd` (default: `"/etc/httpd/conf/htpasswd-kibana"`)

    Path to the htpasswd file for Kibana.

- `kibana_credentials` (default: `"- username: 'operator'
                                     password: 'changeme'"`)

    Hash with username and password for Kibana access to configure in the htpasswd file.

- `kibana_httpd_conf` (default: `"{{ opstools_apache_config_dir }}/kibana.conf"`)

    Path to the Apache configuration file for Kibana.



Httpd
-----

This role installs the Apache web server and associated modules.

Actions defined on the role
+++++++++++++++++++++++++++

- Install httpd
- Install httpd modules
- Allow apache proxy connections
- Ensure httpd configuration directory exists
- Ensure httpd configuration parts directory exists
- Enable httpd service


Configuration
+++++++++++++

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



Grafana
-------

Configuration
+++++++++++++

- `grafana_package_name` (default: `"grafana"`)



- `grafana_server_bind` (default: `"localhost"`)

    This is address to which grafana should bind.
    # Use "0.0.0.0" to listen on all interfaces; use "localhost" to allow
    # access from the local system only.

- `grafana_server_address` (default: `"{{ grafana_server_bind }}"`)

    This is the address to which clients should connect to access Grafana
    (we can't always use grafana_server_bind for that because 0.0.0.0 is
    not an address to which we can connect).
    Note: this needs to be reachable from the node running ansible-playbook

- `grafana_port` (default: `3001`)

    The port on which Grafana should listen.

- `grafana_username` (default: `"admin"`)

    grafana admin username

- `grafana_password` (default: `"admin"`)

    grafana password



Actions defined on the role
+++++++++++++++++++++++++++

- Remove grafana gpg key
- Enable grafana repository
- Add rpm key for grafana repo
- Install grafana
- Configure grafana server section
- Enable grafana
- Create appropriate firewall rules



Actions defined on the role
+++++++++++++++++++++++++++

- Install grafana configuration for Apache
- Configure default redirect
- wait for grafana to be started
- check if datasource added
- create data source for grafana server


Configuration
+++++++++++++

- `grafana_proxy_dest` (default: `"http://{{ grafana_bind }}:{{ grafana_port }}"`)

    URL for backend Grafana service.

- `grafana_httpd_conf` (default: `"{{ opstools_apache_config_dir }}/grafana.conf"`)

    Path to the Apache configuration snippet for the Grafana proxy.

- `grafana_path` (default: `"/grafana"`)

    URL path at which to host Grafana.

- `gauth` (default: `"https://{{grafana_username}}:{{grafana_password}}@"`)

    helper for API access



Actions defined on the role
+++++++++++++++++++++++++++

- Install graphite
- Check if graphitedb already created
- Create database for graphite
- Enable services
- Tweak httpd config
- Listen on port 8080
- Change port on graphite conf
- Create appropriate firewall rules



Configuration
+++++++++++++

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

- `fluentd_owner` (default: `"root"`)

    User that will own Fluentd config files.

- `fluentd_group` (default: `"fluentd"`)

    Group that will own Fluentd config files.

- `fluentd_config_mode` (default: `416`)

    File mode for Fluentd configuration files.

- `fluentd_config_dir_mode` (default: `488`)

    File mode for Fluentd configuration directories.

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



Fluentd/Syslog
--------------

This roles installs the necessary configuration to send logs from the
local syslog server to a Fluentd instance.

Actions defined on the role
+++++++++++++++++++++++++++

- Install fluentd rsyslog config
- Install fluentd syslog source


Configuration
+++++++++++++

- `fluentd_syslog_bind_address` (default: `"127.0.0.1"`)

    Address on which to listen for syslog messages.

- `fluentd_syslog_port` (default: `5140`)

    Port on which to listen for syslog messages.

- `fluentd_syslog_tag` (default: `"system.messages"`)

    Fluentd tag to apply to syslog messages.



Fluentd
-------

`Fluentd <http://www.fluentd.org/>`__ is a log collection tool. It can
collect logs from a variety of sources, filter them, and send them to a
variety of destinations, including remote Fluentd instances.

We use Fluentd to receive logs from remote Fluentd clients and deliver
them to
`Elasticsearch <https://www.elastic.co/products/elasticsearch>`__.

Actions defined on the role
+++++++++++++++++++++++++++

- Install fluentd package
- Install fluentd plugins
- Ensure fluentd configuration directory exists
- Ensure fluentd config.d directory exists
- Create fluentd.conf
- Install fluentd certificate
- Activate fluentd service



Fluentd/Server
--------------

This role configures a Fluentd listener that will listen for remote
connections from other Fluentd clients.

Actions defined on the role
+++++++++++++++++++++++++++

- Install fluentd plugins (server)
- Set fluentd_port fact (non-ssl)
- Set fluentd_port fact (ssl)
- Install non-ssl aggregator endpoint
- Install ssl aggregator endpoint
- Install fluentd private key
- Create appropriate firewall rules


Configuration
+++++++++++++

- `fluentd_server_plugins` (default: `["rubygem-fluent-plugin-elasticsearch"]`)

    A list of plugins that will be installed on the fluentd server.

- `fluentd_private_key_path` (default: `"{{ fluentd_config_dir }}/ca_key.pem"`)

    Path to the SSL certificate private key.

- `fluentd_server_extraconfig` (default: `{}`)

    Additional fluentd configuration.



Fluentd/Elasticsearch
---------------------

This role contains contains configuration to send logs from Fluentd to
an Elasticsearch instance.

Actions defined on the role
+++++++++++++++++++++++++++

- Install fluentd->elasticsearch config


Configuration
+++++++++++++

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



Firewall
--------

This role manage the way of managing firewall rules. Using either
iptables or firewalld tool. It also has the rules to be applied.

Configuration
+++++++++++++

- `firewall_manage_rules` (default: `true`)

    Set this to False if you do not want the playbooks to make changes
    to the system firewall.

- `force_ipv6` (default: `false`)

    Force the use of ipv6

- `firewall_data` (default: `{"redis_hosts": [{"protocol": "tcp", "port": "{{ redis_listen_port }}"}], "elastic_hosts": [{"protocol": "tcp", "port": "{{ elasticsearch_port }}"}], "uchiwa_hosts": [{"source": "{{ uchiwa_bind }}", "protocol": "tcp", "port": "{{ uchiwa_port }}"}, {"protocol": "tcp", "port": "{{ opstools_apache_http_port }}"}, {"protocol": "tcp", "port": "{{ opstools_apache_https_port }}"}], "fluent_hosts": [{"protocol": "tcp", "port": "{{ fluentd_port|default(24224) }}"}, {"protocol": "udp", "port": "{{ fluentd_port|default(24224) }}"}], "kibana_hosts": [{"source": "{{ kibana_server_bind }}", "protocol": "tcp", "port": "{{ kibana_server_port }}"}, {"protocol": "tcp", "port": "{{ opstools_apache_http_port }}"}, {"protocol": "tcp", "port": "{{ opstools_apache_https_port }}"}], "grafana_hosts": [{"protocol": "tcp", "port": "{{ opstools_apache_http_port }}"}, {"protocol": "tcp", "port": "{{ opstools_apache_https_port }}"}], "graphite_hosts": [{"protocol": "tcp", "port": "{{ graphite_port }}"}], "rabbit_hosts": [{"protocol": "tcp", "port": "{{ rabbitmq_port }}"}, {"protocol": "tcp", "port": "{{ rabbitmq_ssl_port }}"}], "collectd_hosts": [{"protocol": "tcp", "port": "{{ collectd_listen_port }}"}], "sensu_hosts": [{"protocol": "tcp", "port": "{{ sensu_api_port }}"}]}`)

    A lists of hashes containing data for configuration firewall rules
    to be created on each host groups
    .. code-block:: json

        { host_group: [{port: PORT, source: SOURCE, protocol:PROTOCOL},
                       {port: PORT, protocol:PROTOCOL}]}



Firewall/Gather
---------------

This role gathers facts from host regarding firewall resources

Actions defined on the role
+++++++++++++++++++++++++++

- Determine firewall provider
- Set use_firewalld fact
- Set use_iptables fact



Firewall/Commit
---------------

This role instantiates the firewall rules that were setup in
firewall\_data

Actions defined on the role
+++++++++++++++++++++++++++

- Enable service ports via iptables
- Enable service ports via firewalld



Elasticsearch
-------------

`Elasticsearch <https://www.elastic.co/products/elasticsearch>`__ is a
search and analytics engine used by Ops Tools to collect, index, search,
and analyze logs.

Configuration
+++++++++++++

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



Elasticsearch/server
--------------------

Install the
`Elasticsearch <https://www.elastic.co/products/elasticsearch>`__ engine
and all its dependencies.

`Elasticsearch <https://www.elastic.co/products/elasticsearch>`__ is a
search and analytics engine used by Ops Tools to collect, index, search,
and analyze logs.

Actions defined on the role
+++++++++++++++++++++++++++

- Install java package
- Enable elasticsearch repository
- Install elasticsearch package
- Install elasticsearch service configuration
- Install elasticsearch configuration
- Activate elasticsearch service
- Create appropriate firewall rules



Collectd
--------

Configuration
+++++++++++++

- `collectd_package_name` (default: `"collectd"`)

    name of the collectd package.

- `collectd_service_name` (default: `"collectd"`)

    name of the collectd service.

- `collectd_plugin_packages` (default: `["collectd-disk", "collectd-ipmi", "collectd-iptables", "collectd-sensors"]`)

    a list of additional packages to install (presumably ones that
    provide collectd plugins).

- `collectd_plugin_config` (default: `{}`)

    additional plugin configuration for collectd.  each key in this
    dictionary will be used as the base of a filename, and the contents
    of that file will be the corresponding value.

- `collectd_config_dir` (default: `"/etc/collectd.d"`)

    where collectd configuration snippets are located.

- `collectd_config_file` (default: `"/etc/collectd.conf"`)

    path to the main collectd configuration file

- `collectd_auth_file` (default: `"/etc/collectd.auth"`)

    path to the file that will contain collectd network authentication
    credentials.

- `collectd_config_owner` (default: `"root"`)

    owner of collectd config files and directories

- `collectd_auth_file_mode` (default: `"0600"`)

    mode for collectd credentials file

- `collectd_config_file_mode` (default: `"0600"`)

    mode for collectd config files

- `collectd_config_dir_mode` (default: `"0700"`)

    mode for collect config directory

- `graphite_host` (default: `"localhost"`)

    target address for write_graphite plugin

- `graphite_port` (default: `2003`)

    target port for write_graphite plugin

- `collectd_listen_address` (default: `"0.0.0.0"`)

    address on which collectd should listen for network connections

- `collectd_listen_port` (default: `25826`)

    port on which collectd should listen for network connections

- `collectd_securitylevel` (default: `"None"`)

    This can be one of None, Sign, or Encrypt.

- `collectd_users` (default: `{}`)

    a dictionary of user: password pairs that will be written to
    the collectd credentials file when using Sign or Encrypt
    securitylevel.

- `collectd_purge` (default: `true`)

    if true, remove all configuration snippets from collectd_config_dir

- `collectd_purge_config` (default: `true`)

    if true, replace main collectd.conf with generated config



Actions defined on the role
+++++++++++++++++++++++++++

- Install collectd
- Install collectd plugin packages
- Purge collectd configuration file
- Ensure collectd configuration file exists
- Purge collectd configuration directory
- Ensure collectd configuration directory exists
- Generate write_graphite configuration
- Generate collectd network server configuration
- Generate collectd plugin configuration
- Generate collectd credentials file
- Set collectd_tcp_network_connect
- Enable collectd service
- Create appropriate firewall rules



Chrony
------

Installs and configures an NTP client
(`Chrony <https://chrony.tuxfamily.org/>`__) to ensure that the server
keeps correct time. Clock skew between the server and clients can cause
unexpected behaviors.

Actions defined on the role
+++++++++++++++++++++++++++

- Install chrony package
- Generate chrony configuration
- Activate chrony service


Configuration
+++++++++++++

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


Integration with TripleO
------------------------

The `TripleO <http://tripleo.org/>`__ installer for OpenStack includes support for Fluentd and
Sensu clients. See :doc:`../tripleo_integration`.

Contributing
------------

If you encounter problems with or have suggestions about
opstools-ansible, open an issue on our `Github issue
tracker <https://github.com/centos-opstools/opstools-ansible/issues>`__.

If you would like to contribute code, documentation, or other changes to
the project, please read the :doc:`../developers`.

License
-------

Copyright 2016 `Red Hat, Inc. <http://www.redhat.com/>`__

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

-  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

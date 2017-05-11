Integrating opstools-ansible with a TripleO deployment
======================================================

Before you begin
----------------

This guide assumes that you are working with the **OpenStack Newton**
release.

For the purpose of creating some concrete examples, this document
assumes that you have deployed your opstools-ansible environment using
the following inventory:

::

    ops0 ansible_host=192.168.10.10
    ops1 ansible_host=192.168.10.20

    [am_hosts]
    ops0

    [logging_hosts]
    ops1

And the following configuration:

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

Configure TripleO
~~~~~~~~~~~~~~~~~

Once your opstools environment is running, create a configuration file
for your TripleO environment that will point the Sensu and Fluentd
agents at the opstools hosts. Look at the
`logging <https://github.com/openstack/tripleo-heat-templates/blob/master/environments/logging-environment.yaml>`__
and
`monitoring <https://github.com/openstack/tripleo-heat-templates/blob/master/environments/monitoring-environment.yaml>`__
environment files for a list of available parameters.

Given the example configuration presented earlier in this document, you
might end up with something like this (in a file we'll call
``params.yaml``):

::

    parameter_defaults:

      LoggingServers:
        - host: 192.168.10.20
          port: 24284

      LoggingUsesSSL: true

      # This must match the fluentd_shared_key key setting you
      # used in your Ansible configuration.
      LoggingSharedKey: secret

      # This must match the certificate you used for the
      # fluentd_ca_cert setting in your Ansible configuration.
      LoggingSSLCertificate: |
        -----BEGIN CERTIFICATE-----
        -----END CERTIFICATE-----

      MonitoringRabbitHost: 192.168.10.10
      MonitoringRabbitUsername: sensu
      MonitoringRabbitPassword: sensu

Run overcloud deploy command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deploy your TripleO environment. In addition to whatever command line
options you normally use, you will need to include the
``monitoring-environment.yaml`` file (if you are configuring
availability monitoring), and ``logging-environment.yaml`` file (if you
arae configuring logging), and the ``params.yaml`` file described in the
previous step. Your ``overcloud deploy`` command line should look
something like:

::

    openackstack overcloud deploy ... \
      -e /usr/share/openstack-tripleo-heat-templates/environments/monitoring-environment.yaml \
      -e /usr/share/openstack-tripleo-heat-templates/environments/logging-environment.yaml \
      -e params.yaml

When the deployment completes, you should see logs appearing in Kibana
on your opstools server (``https://192.168.10.20/kibana``) and you
should see the results of Sensu checks in Uchiwa
(``https://192.168.10.10/uchiwa``).

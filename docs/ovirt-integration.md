# Integrating opstools-ansible with oVirt

Mission: To configure oVirt hosts to send metrics data to a central elasticsearch
store.

More information: [oVirt] [oVirt Metrics]

[oVirt]: http://ovirt.org
[oVirt Metrics]: http://www.ovirt.org/develop/release-management/features/engine/metrics-store/

## General architecture

See also [oVirt architecture] for a general overview.

In a typical oVirt setup, there are these components:

1. one Engine

This is a java/wildfly application, managing the entire setup.
It is set up on its own machine.

2. One or more hosts (nodes), on which we run virtual machines (VMs)

3. Other components, e.g. storage, network, etc., that are unrelated to current document

4. One (perhaps more, in the future) Metrics Store

Using opstools-ansible, with a suitable configuration, it is possible to configure
the hosts to send metrics to the metrics store.

On each host, we run a collectd instance. This instance collects metrics using
its own plugins, and also accepts metrics data from VDSM, which connects to it
using the statsd plugin. It writes the metrics it collected to a local fluentd,
using write_http.

Further, on each host, we run a local fluentd instance. This instance gets
metrics from collectd, processes them, and forwards them to a remote fluentd
on the metrics store, using secure-forward.

On the metrics store, we run a central fluentd, that receives metrics data from
the fluentd instances on each of the hosts, using secure-forward, and writes them
to elasticsearch.

The ansible playbook doing all these configurations should run on the engine
machine, so that it has access to the engine. From the engine, it gets the
list of hosts, and a set of parameters - including the central fluentd machine
address, port, etc.

[oVirt architecture]: https://www.ovirt.org/documentation/architecture/architecture/


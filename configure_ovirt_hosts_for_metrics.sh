#!/bin/sh

ansible-playbook playbook.yml -i inventory -e @config.yml -l ovirt_up_metrics_hosts

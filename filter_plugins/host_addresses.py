"""
Copyright 2016 Red Hat Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from ansible.errors import AnsibleFilterError


def host_addresses(hosts, hostvars, ip_version='ipv4'):
    try:
        return [
            hostvars[item]['ansible_default_{}'.format(ip_version)]['address']
            for item in hosts
            if (
                item in hostvars and
                'ansible_default_{}'.format(ip_version) in hostvars[item]
            )
        ]
    except Exception as ex:
        raise AnsibleFilterError(
            "Failed to format host address from data '{}' "
            "due to:\n{}".format(hosts, ex)
        )


class FilterModule(object):
    def filters(self):
        return {
            'host_addresses': host_addresses
        }

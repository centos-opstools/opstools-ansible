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

import socket
from ansible.errors import AnsibleFilterError


def is_ipv6(value):
    try:
        socket.inet_pton(socket.AF_INET6, value)
        return True
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET, value)
        except socket.error:
            raise AnsibleFilterError(
                'Given value is not IP address: {}'.format(value)
            )
        return False


class FilterModule(object):
    def filters(self):
        return {
            'is_ipv6': is_ipv6
        }

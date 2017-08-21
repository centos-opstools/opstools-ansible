plugin_type: install
description: install opstools server
subparsers:
   opstools:
       help: Install OpsTools servers side on Openstack deployments
       include_groups: ["Ansible options", "Inventory", "Common options", "Answers file"]
       groups:
           - title: OpsTools
             options:
                 host:
                     type: Value
                     help: |
                         Host address that will be binded by opstools servers.
                         __LISTYAMLS__
                     default: default

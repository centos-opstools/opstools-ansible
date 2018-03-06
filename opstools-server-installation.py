#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import sys


class ConfigInstaller(object):

    def __init__(self):
        self.options = []
        self.home = os.environ['HOME']
        self.command = ''

    def parse_arguments(self):
        formatter = argparse.RawDescriptionHelpFormatter
        uses = '''Examples:
 *Install availability monitoring and centralized logging on localhost:
    opstools-server-installation --am-hosts localhost --log-hosts localhost
 *Install performance monitoring on a server IP:
    opstools-server-installation --pm-hosts IP
 *Install performance and availability monitoring on a server:
    opstools-server-installation --pm-hosts IP --am-hosts IP
 *Just create the inventory and overwritten if it exits:
    opstools-server-installation -f --no-x '''

        parser = argparse.ArgumentParser(prog='opstools-server-installation',
                                         formatter_class=formatter,
                                         description=(
                                             'Script to set up the'
                                             ' operational servers.'
                                         ),
                                         epilog=uses)
        parser.add_argument('-i', '--inventory',
                            dest='opstoolinvpath',
                            help=(
                                'Opstool inventory path. '
                                'default= ~/.opstools.inventory'
                            ),
                            default=self.home + '/.opstools.inventory')
        parser.add_argument('--pm-hosts',
                            dest='pm_hosts',
                            action='append',
                            help=(
                                'Performance monitoring server IP. '
                                'default = []'
                            ),
                            default=[])
        parser.add_argument('--am-hosts',
                            dest='am_hosts',
                            action='append',
                            help=(
                                'Available monitoring server IP. '
                                'default = []'
                            ),
                            default=[])
        parser.add_argument('--log-hosts',
                            dest='logging_hosts',
                            action='append',
                            help=(
                                'Logging monitoring server IP. '
                                'default = localhost'
                            ),
                            default=[])
        parser.add_argument('-qs',
                            dest='ooo_ssh_ansible',
                            help=(
                                'Quickstart config path. '
                                'default=~/.quickstart/ssh.config.ansible'
                            ),
                            default='{}/.quickstart/ssh.config.ansible'.format(
                                    self.home))
        parser.add_argument('--playbook',
                            dest='playbook',
                            type=str,
                            help='Playbook to run',
                            choices=('playbook.yml',
                                     'playbook-post-install.yml'),
                            default='playbook.yml')
        parser.add_argument('-f',
                            dest='force',
                            help='Overwrite the config file',
                            action='store_true',
                            default=False)
        parser.add_argument('-e',
                            dest='parameters',
                            type=str,
                            help='Extra parameters file.yml')
        parser.add_argument('--no-x',
                            dest='no_exec',
                            default=False,
                            action='store_true',
                            help='Dont run ansible-playbook')
        parser.add_argument('--data-path',
                            dest='data_path',
                            default='/usr/share/opstools-ansible',
                            help=(
                                'Path where the playbooks, roles, inventory '
                                ' and so on are located. default location is '
                                '/usr/share/opstools-ansible'
                            ))
        self.options = parser.parse_args()
        self.parser = parser

    def _parse_hosts(self):
        hosts = {'all': [],
                 'split': {
                           'pm_hosts': [],
                           'am_hosts': [],
                           'logging_hosts': []
                          }}
        for host_type in ('pm_hosts', 'am_hosts', 'logging_hosts'):
            for host in getattr(self.options, host_type):
                hosts['split'][host_type].append(host)
                hosts['all'].append(host)
        return hosts

    def _create_hosts_file(self):
        _path = os.path.join(self.options.opstoolinvpath, 'hosts')
        hosts = self._parse_hosts()
        if ((not os.path.exists(_path) or self.options.force) and
           len(hosts['all']) > 0):
            with open(_path, 'w') as hosts_file:
                for host_type in hosts['split'].keys():
                    hosts_file.write('[{}]\n'.format(host_type))
                    for host in hosts['split'][host_type]:
                        hosts_file.write('{}\n'.format(host))
                    hosts_file.write('\n')
                hosts_file.write("[targets]\n")
                for host in set(hosts['all']):
                    if host in ('localhost', 'localhost6', '127.0.0.1', '::1'):
                        hosts_file.write('{} ansible_connection=local'
                                         '\n'.format(host))
                    else:
                        hosts_file.write('{} ansible_connection=ssh '
                                         'ansible_user=root\n'.format(
                                             host
                                             )
                                         )
                hosts_file.write('undercloud_host ansible_user=stack '
                                 'ansible_host=undercloud '
                                 'ansible_ssh_extra_args=\'-F {}\'\n'.format(
                                     self.options.ooo_ssh_ansible
                                     )
                                 )
        else:
            print('\x1b[34m INFO: the inventory file was not'
                  ' created/updated\x1b[0m')

    def create_configuration(self):
        try:
            # destination file
            _dest_f = os.path.join(self.options.opstoolinvpath,
                                   'structure')
            # origin file
            _source_f = os.path.join(self.options.data_path,
                                     'inventory',
                                     'structure')
            if not os.path.isdir(self.options.opstoolinvpath):
                os.makedirs(self.options.opstoolinvpath)
            if not os.path.exists(_dest_f) or self.options.force:
                shutil.copy(_source_f, _dest_f)
            self._create_hosts_file()
        except Exception:
            print('Error: There was a problem creating the inventory')
            self.parser.print_help()
            sys.exit(-1)

    def create_command(self):
        self.command = (
            'ansible-playbook -i {inventory} {path}/{playbook}'.format(
                inventory=self.options.opstoolinvpath,
                path=self.options.data_path,
                playbook=self.options.playbook
            )
        )

        if self.options.parameters:
            if os.path.exists(self.options.parameters):
                self.command = '{command} -e {parameters}'.format(
                    command=self.command,
                    parameters=self.options.parameters)
            else:
                print('Error: The file {parameters} does not exits'
                      .format(parameters=self.options.parameters))
                self.parser.print_usage()
                sys.exit(-1)


def main():
    config = ConfigInstaller()
    config.parse_arguments()
    config.create_configuration()
    config.create_command()
    if not config.options.no_exec:
        subprocess.call(config.command, shell=True)
    else:
        print('To continue:\n\t{}'.format(config.command))


if __name__ == "__main__":
    main()

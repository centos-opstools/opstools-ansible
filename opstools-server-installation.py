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
 *Enable Availability Monitoring and centralized logging
will be installed on localhost):
    opstools-server-installation -l -a
 *Install centralized logging on a server an availability monitoring
on localhost:
    opstools-server-installation -l --log-hosts IP
 *Install performance and availability monitoring on a server:
    opstools-server-installation -p -pm-hosts IP -a -am-hosts IP
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
                                'Opstool inventory path.'
                                'default= ~/.opstools.inventory'
                            ),
                            default=self.home + '/.opstools.inventory')
        parser.add_argument('--pm-hosts',
                            dest='pm_hosts',
                            action='append',
                            help=(
                                'Performance monitoring server IP.'
                                'default = localhost'
                            ),
                            default=[])
        parser.add_argument('-p', '--performance-monitoring',
                            dest='pm',
                            help=(
                                'Enable Performance monitoring.'
                                'default=disabled'
                            ),
                            default=False,
                            action='store_true')
        parser.add_argument('--am-hosts',
                            dest='am_hosts',
                            action='append',
                            help=(
                                'Available monitoring server IP.'
                                'default = localhost'
                            ),
                            default=[])
        parser.add_argument('-a', '--availability-monitoring',
                            dest='am',
                            help=(
                                'Enable Available  monitoring.'
                                'default=disable'
                            ),
                            default=False,
                            action='store_true')
        parser.add_argument('--log-hosts',
                            dest='logging_hosts',
                            action='append',
                            help=(
                                'Logging monitoring server IP.'
                                'default = localhost'
                            ),
                            default=[])
        parser.add_argument('-l', '--centralized-logging',
                            dest='cl',
                            help=(
                                'Enable logging monitoring.'
                                'default=disable'
                            ),
                            default=False,
                            action='store_true')
        parser.add_argument('-qs',
                            dest='ooo_ssh_ansible',
                            help=(
                                'Quickstart config path.'
                                'default=~/.quickstart/ssh.config.ansible'
                            ),
                            default=self.home +
                            '/.quickstart/ssh.config.ansible')
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
        self.options = parser.parse_args()

    def _create_hosts_file(self):
        _path = os.path.join(self.options.opstoolinvpath, 'hosts')
        if not os.path.exists(_path) or \
           self.options.force:
            hosts_file = open(_path, 'w')
            hosts = []
            if (self.options.pm):
                hosts_file.write('[pm_hosts]\n')
                if len(self.options.pm_hosts) == 0:
                    self.options.pm_hosts = ['localhost']
                for host in self.options.pm_hosts:
                    hosts_file.write(host)
                    hosts_file.write('\n')
                    hosts.append(host)
                hosts_file.write('\n')
            if (self.options.am):
                hosts_file.write('[am_hosts]\n')
                if len(self.options.am_hosts) == 0:
                    self.options.am_hosts = ['localhost']
                for host in self.options.am_hosts:
                    hosts_file.write(host)
                    hosts_file.write('\n')
                    hosts.append(host)
                hosts_file.write('\n')
            if (self.options.cl):
                hosts_file.write('[logging_hosts]\n')
                if len(self.options.logging_hosts) == 0:
                    self.options.logging_hosts = ['localhost']
                for host in self.options.logging_hosts:
                    hosts_file.write(host)
                    hosts_file.write('\n')
                    hosts.append(host)
                hosts_file.write('\n')

            hosts_file.write("[targets]\n")
            for host in set(hosts):
                if "localhost" == host:
                    hosts_file.write('localhost ansible_connection=local\n')
                else:
                    hosts_file.write(host +
                                     ' ansible_connection=' +
                                     'ssh ansible_user=root\n')
            hosts_file.write('undercloud_host ansible_user=stack' +
                             ' ansible_host=undercloud ')
            hosts_file.write('ansible_ssh_extra_args=\'-F "')
            hosts_file.write(self.options.ooo_ssh_ansible+'"\'\n')
            hosts_file.close()

    def create_configuration(self):
        try:
            # destination file
            _dest_f = os.path.join(self.options.opstoolinvpath,
                                   'structure')
            # origin file
            _source_f = os.path.join('inventory',
                                     'structure')
            if not os.path.isdir(self.options.opstoolinvpath):
                os.makedirs(self.options.opstoolinvpath)
            if not os.path.exists(_dest_f) or self.options.force:
                shutil.copy(_source_f,
                            _dest_f)
            self._create_hosts_file()
        except Exception:
            print('There was a problem creating the inventory')
            sys.exit(-1)

    def create_command(self):
        self.command = 'ansible-playbook -i {inventory} {playbook}'.format(
            inventory=self.options.opstoolinvpath,
            playbook=self.options.playbook)

        if self.options.parameters:
            if os.path.exists(self.options.parameters):
                self.command = '{command} -e {parameters}'.format(
                    command=self.command,
                    parameters=self.options.parameters)
            else:
                print('The file {parameters} does not exits'.format(
                      parameters=self.options.parameters))
                sys.exit(-1)


def main():
    config = ConfigInstaller()
    config.parse_arguments()
    config.create_configuration()
    config.create_command()
    if not config.options.no_exec:
        subprocess.call(config.command, shell=True)


if __name__ == "__main__":
    main()

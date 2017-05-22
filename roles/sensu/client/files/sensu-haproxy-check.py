#!/usr/bin/python

import argparse
import json
import requests
import sys

from requests.auth import HTTPBasicAuth


def status2text(status):
    '''Returns correct return code for haproxy stats record.'''
    rc = 1
    if status in ('UP', 'OPEN'):
        rc = 0
    if status == 'DOWN' or status == 'DOWN 1/2':
        rc = 2
    return (rc, status)


def parse_arguments():
    parser = argparse.ArgumentParser(description='HAProxy stats checker.')

    parser.add_argument('--haproxy-auth', required=True,
                        help='HAProxy user:password')
    parser.add_argument('--haproxy-uri', required=True,
                        help='url to HAProxy')
    parser.add_argument('--sensu-uri', required=True,
                        help='url to Sensu API to insert results')
    parser.add_argument('--sensu-max-errors', type=int, default=3,
                        help='maximum amount of consecitive errors,'
                             ' by default 3')
    parser.add_argument('--haproxy-timeout', type=int, default=2,
                        help='timeout to request stats to haproxy,'
                             ' by default 2 sec')
    parser.add_argument('--sensu-timeout', type=int, default=2,
                        help='timeout to send data to sensu,'
                             ' by default 2 sec')
    parser.add_argument('--data-by-service',
                        action='store_true', default=False,
                        help='group result data by service instead '
                             'of by node type')

    options = parser.parse_args()
    try:
        user_password = options.haproxy_auth.split(":")
        options.user = user_password[0]
        options.password = user_password[1]
    except Exception:
        print(
            'There is a problem with the auth argument. '
            'The syntax is \'user:password\''
        )
        sys.exit(2)
    return options


def send_data(sensu_api, data, timeout):
    try:
        result = requests.post('{}/results'.format(sensu_api),
                               headers={'content-type': 'application/json'},
                               data=json.dumps(data),
                               timeout=timeout)
    except Exception:
        rc = 1
    else:
        if result.status_code != 202:
            rc = 1
        else:
            rc = 0
    return rc


def main(options):
    try:
        req = requests.get(
            '{}/haproxy?stats;csv'.format(options.haproxy_uri),
            auth=HTTPBasicAuth(options.user, options.password),
            timeout=options.haproxy_timeout)
    except requests.exceptions.Timeout as ex:
        result = (2, str(ex.message.reason.args[1]))
    except requests.exceptions.ConnectionError:
        result = (2, 'Could not connect to '
                     '{}/haproxy?stats;csv'.format(options.haproxy_uri))
    else:
        if req.status_code != 200:
            result = (2, 'HAProxy response: {}'.format(req.status))
        else:
            errors = 0
            result = (0, 'status OK')
            for line in req.content.split('\n'):
                if line.startswith('#'):
                    # skip commented lines (usually first line)
                    continue
                words = line.split(',')
                if (len(words) < 18):
                    # skip invalid lines
                    continue
                host = words[1]
                service = words[0]
                status, status_str = status2text(words[17])
                if options.data_by_service:
                    data = {'source': 'HAProxy.{}'.format(service),
                            'name': host, 'output': status_str,
                            'status': status}
                else:
                    data = {'source': 'HAProxy.{}'.format(host),
                            'name': service, 'output': status_str,
                            'status': status}
                errors += send_data(
                    options.sensu_uri,
                    data,
                    options.sensu_timeout)
                if errors >= options.sensu_max_errors:
                    result = (2, 'Consecitive service error '
                                 'threadshold reached')
                    break
            if errors > 0:
                result = (1, 'Could not insert some data to sensu')
    return result


if __name__ == '__main__':
    rc, msg = main(parse_arguments())
    print(msg)

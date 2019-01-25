#!/usr/bin/python

import argparse
import json
import re
import requests
import sys


def send_data(url, data, timeout, cache):
    # update cache
    records = {}
    with open(cache, 'r') as cf:
        for line in cf:
            if not line:
                continue
            client, checklist = line.split(':::')
            records[client.strip()] = set(checklist.strip().split(','))
    records.setdefault(data['source'].strip(), set()).add(data['name'].strip())
    with open(cache, 'w') as cf:
        for client, checks in records.items():
            cf.write('{}:::{}'.format(client, ','.join(checks)))
    # create container check
    requests.post('{}/results'.format(url),
                  headers={'content-type': 'application/json'},
                  data=json.dumps(data),
                  verify=False,
                  timeout=timeout)


def delete_data(url, client, timeout, cache):
    # read cache
    records = {}
    with open(cache, 'r') as cf:
        for line in cf:
            if not line:
                continue
            cl, checklist = line.split(':::')
            records[cl.strip()] = set(checklist.strip().split(','))
    # delete container checks
    for check in records[client]:
        requests.delete('{}/results/{}/{}'.format(url, client, check),
                        verify=False,
                        timeout=timeout)
        requests.delete('{}/events/{}/{}'.format(url, client, check),
                        verify=False,
                        timeout=timeout)
    # update cache
    del records[client.strip()]
    with open(cache, 'w') as cf:
        for cl, checks in records.items():
            cf.write('{}:::{}'.format(cl, ','.join(checks)))


def main():
    parser = argparse.ArgumentParser(description='Handler script for '
                                     'check-docker-health check '
                                     'from TripleO nodes.')
    parser.add_argument('--sensu-api', required=True,
                        help='Sensu API base URL')
    parser.add_argument('--cache', help='Data cache file',
                        default='/tmp/.sensu-check-docker-health-cache')
    parser.add_argument('--timeout', type=int, default=1)
    parser.add_argument('--data-separator', default=' ; ',
                        help='Separator of check output data')
    options = parser.parse_args()

    # $(docker inspect --format='{{.Name}}' $i) ($i):
    # $(docker inspect --format='{{(index .State.Health.Log 0).Output}}' $i)
    regex = re.compile(r'[\s\/]*(?P<name>.*) \((?P<cid>.*)\)\:\s*(?P<msg>.*)')
    event = json.loads(sys.stdin.read())
    try:
        with open(options.cache, 'r') as cf:
            pass
    except IOError:
        with open(options.cache, 'w') as cf:
            cf.write('')

    if event['action'] == 'create':
        for line in event['check']['output'].split(options.data_separator):
            if not line:
                continue
            match = regex.match(line)
            if not match:
                continue
            data = {'source': event['client']['name'],
                    'name': match.group('name'),
                    'output': '({}): {}'.format(match.group('cid'),
                                                match.group('msg')),
                    'status': 2}
            send_data(options.sensu_api, data, options.timeout, options.cache)
    elif event['action'] == 'resolve':
        delete_data(options.sensu_api, event['client']['name'],
                    options.timeout, options.cache)


if __name__ == '__main__':
    main()

#!/usr/bin/python

import sys
import argparse
import json
import requests
from requests.auth import HTTPBasicAuth


def _status2text(status):
    if status == 'UP':
        return (1, 'OK')
    if status == 'DOWN' or status == 'DOWN 1/2':
        return (2, 'ERROR')
    return (3, 'UNKOWN')


def _parseArguments():
    parser = argparse.ArgumentParser(description='HAProxy stats checker.')

    parser.add_argument('--auth', metavar='auth', type=str, required=True,
                        help='user:password')
    parser.add_argument('--haproxy', metavar='haproxy', type=str,
                        required=True,
                        help='ha proxy uri, http://10.0.1.200')
    parser.add_argument('--sensu_api', metavar='sensu_api', type=str,
                        required=True,
                        help='sensu api to insert results, http://10.0.1.200')
    parser.add_argument('--sensu_max_errors', type=int,
                        default=3, metavar='sensu_max_errors',
                        help='maximum amount of consecutive errors,'
                             ' by default 3')
    parser.add_argument('--ha_timeout', metavar='ha_timeout',
                        type=int, default=2,
                        help='timeout to request stats to haproxy,'
                             ' by default 2 sec')
    parser.add_argument('--sensu_timeout', metavar='sensu_timeout', type=int,
                        default=2,
                        help='timeout to send data to sensu,'
                             ' by default 2 sec')

    options = parser.parse_args()
    user_password = options.auth.split(":")
    options.user = user_password[0]
    options.password = user_password[1]
    return options


def _sendData2Sensu(sensu_api, headers, data, data_sent,
                    prev_errors, error, timeout):
    try:
        result = requests.post(sensu_api, headers=headers,
                               data=json.dumps(data), timeout=timeout)
        data_sent = data_sent + 1
        if result.status_code != 202:
            prev = prev_errors + 1
            error = 1
        else:
            prev = 0
    except:
        error = 1
        prev = prev_errors + 1
    return (data_sent, prev, error)

options = _parseArguments()

try:
    req = requests.get(options.haproxy+"/haproxy?stats;csv",
                       auth=HTTPBasicAuth(options.user, options.password),
                       timeout=options.ha_timeout)
except requests.exceptions.Timeout as to:
    print "ERROR - "+to.message.reason.args[1]
    sys.exit(2)
except requests.exceptions.ConnectionError as co:
    print 'ERROR - Could not connect to '+options.haproxy+"/haproxy?stats;csv"
    sys.exit(2)

if req.status_code != 200:
    print str(req.status_code) + ' - HAProxy response'
    sys.exit(2)

options.sensu_api = options.sensu_api + '/results'

lines = req.content.split('\n')

headers = {'content-type': 'application/json'}

services_sent = 0
services_prev_errors = 0
nodes_sent = 0
nodes_prev_errors = 0
total = 0
error_services = 0
error_nodes = 0
result = (0, 'status OK')


for line in lines:
    words = line.split(',')
    if (len(words) < 18):
        break
    host = words[1]
    service = words[0]
    (status, status_str) = _status2text(words[17])
    data_by_service = {'source': service, 'name': host,
                       'output': status_str, 'status': status}
    data_by_node = {'source': host, 'name': service,
                    'output': status_str, 'status': status}
    total = total + 1
    # Sending Service data
    (services_sent,
     services_prev_errors,
     error_services) = _sendData2Sensu(options.sensu_api,
                                       headers,
                                       data_by_service,
                                       services_sent,
                                       services_prev_errors,
                                       error_services,
                                       options.sensu_timeout)
    if services_prev_errors >= options.sensu_max_errors:
        result = (2, 'ERROR - Consecutive service error threadshold reached')
        break
    # Sending Node data
    (nodes_sent,
     nodes_prev_errors,
     error_nodes) = _sendData2Sensu(options.sensu_api,
                                    headers,
                                    data_by_service,
                                    nodes_sent,
                                    nodes_prev_errors,
                                    error_nodes,
                                    options.sensu_timeout)
    if nodes_prev_errors >= options.sensu_max_errors:
        result = (2, 'ERROR - Consecutive node error threadshold reached')
        break

if result[0] != 2:
    if error_services != 0:
        if error_nodes != 0:
            result = (1, 'WARNING - Could not insert some data to sensu')
        else:
            result = (1,
                      'WARNING - Could not insert some service data to sensu')
    else:
        if error_nodes != 0:
            result = (1, 'WARNING - Could not insert some node data to sensu')

print result[1]
sys.exit(result[0])

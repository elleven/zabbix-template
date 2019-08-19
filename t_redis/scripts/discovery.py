#!/bin/env python

import json
from config import REDIS_INSTANCES
from redis import redis
from zabbix import push_to_zabbix
import re

instance_data = []
slave_data = []
keyspace_data = []

for conf in REDIS_INSTANCES:
    r = redis(conf)
    instance_data.append({ '{#PORT}' : r.port })
    for key in r.info.Replication.keys():
        if re.match('slave\d', key):
            slave_data.append({ '{#PORT}' : r.port, '{#SLAVE}' : '{ip}:{port}'.format(ip=r.info.Replication[key]['ip'], port=r.info.Replication[key]['port']) })

    for key in r.info.Keyspace.keys():
        if key.startswith('db'):
            keyspace_data.append({ '{#PORT}' : r.port, '{#KEYSPACE}' : key })

print json.dumps({ 'data' : instance_data })

'''
slave and keyspace discovery
'''
push_to_zabbix('redis-slave-discovery', json.dumps({ 'data' : slave_data }))
push_to_zabbix('redis-keyspace-discovery', json.dumps({ 'data' : keyspace_data }))

#print json.dumps({ 'data' : slave_data })
#print json.dumps({ 'data' : keyspace_data })

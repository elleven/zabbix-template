#!/bin/env python

import re

from config import REDIS_INSTANCES
from redis import redis
from zabbix import push_to_zabbix

import os


for conf in REDIS_INSTANCES:
    r = redis(conf)

    #push info
    for section in r.info.__dict__.keys(): 

        if section == 'Replication':
            for key, value in r.info.Replication.items():
                if re.match('slave\d', key):
                    push_to_zabbix('redis.info[{port}][Replication][slave][{slave}][lag]'.format(port=r.port, slave='{ip}:{port}'.format(ip=value['ip'], port=value['port'])), value['lag'])
                    push_to_zabbix('redis.info[{port}][Replication][slave][{slave}][state]'.format(port=r.port, slave='{ip}:{port}'.format(ip=value['ip'], port=value['port'])), value['state'])

                    #do not push the invalid offset when slave state is not online
                    if value['state'] == "online" and value['offset'] > 0:
                        push_to_zabbix('redis.info[{port}][Replication][slave][{slave}][offset]'.format(port=r.port, slave='{ip}:{port}'.format(ip=value['ip'], port=value['port'])), value['offset'])
                    push_to_zabbix('redis.info[{port}][Replication][slave][{slave}][master_repl_offset]'.format(port=r.port, slave='{ip}:{port}'.format(ip=value['ip'], port=value['port'])), r.info.Replication['master_repl_offset'])
                else:
                    push_to_zabbix('redis.info[{port}][{section}][{key}]'.format(port=r.port, section=section, key=key), value)
        
        elif section == 'Keyspace':
            for key, value in r.info.Keyspace.items():
                if key.startswith('db'):
                    for k, v in value.items():
                        push_to_zabbix('redis.info[{port}][Keyspace][{keyspace}][{k}]'.format(port=r.port, keyspace=key, k=k), v)

        else:
            for key, value in r.info.__dict__[section].items():
                push_to_zabbix('redis.info[{port}][{section}][{key}]'.format(port=r.port, section=section, key=key), value)

    #push latest slowlog id
    if 'id' in r.latest_slowlog.__dict__:
        push_to_zabbix('redis.slowlog.latest.id[{port}]'.format(port=r.port), r.latest_slowlog.id)


    #push config
    push_to_zabbix('redis.config[{port}][{key}]'.format(port=r.port, key='maxclients'), r.config.maxclients)
    if r.config.maxmemory != "0":
        push_to_zabbix('redis.config[{port}][{key}]'.format(port=r.port, key='maxmemory'), r.config.maxmemory)
    push_to_zabbix('redis.config[{port}][{key}]'.format(port=r.port, key='save'), r.config.save)

print "OK"

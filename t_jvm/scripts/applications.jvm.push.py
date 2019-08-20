#!/bin/env python

import traceback
from jstat import JSTAT_GC
from zabbix import push_to_zabbix_by_shell as push_to_zabbix
from exception import PIDNOTExistException
from tigersupervisor import TigerSupervisord,get_socket_path


def getpids():
    result = {}
    sd = TigerSupervisord(get_socket_path())
    for instance in sd.getAllProcessInfo():
        if instance['statename'] == 'RUNNING':
            result.setdefault(instance['name'],instance['pid'])
    return result


for app,pid in getpids().iteritems():
    try:
        jvm = JSTAT_GC(pid)
        for k,v in jvm.gc.iteritems():
            push_to_zabbix('jvm.info[{application}][{header}]'.format(application=app, header=k), v)
    except PIDNOTExistException:
        print traceback.format_exc()
    except:
        print traceback.format_exc()
        push_to_zabbix('applications.jvm.push', traceback.format_exc())        
        raise
#push_to_zabbix('applications.jvm.push', 'OK')
print 'ok'


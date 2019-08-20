#!/usr/bin/env python
import json
from tigersupervisor import TigerSupervisord,get_socket_path


instance_data = []
sd = TigerSupervisord(get_socket_path())

for instance in sd.getAllProcessInfo():
    if instance['statename'] == 'RUNNING':
        instance_data.append({ '{#APPLICATION}' : instance['name'] })

print json.dumps({ 'data' : instance_data })

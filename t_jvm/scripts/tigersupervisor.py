#!/usr/bin/python

import ConfigParser
import xmlrpclib,supervisor.xmlrpc
from config import DEFAULT_SUPERVISOR_CONF


class TigerSupervisord(object):
    def __init__(self,socket):
        self.s = xmlrpclib.ServerProxy('http://127.0.0.1',transport=supervisor.xmlrpc.SupervisorTransport(
                None,None, socket ))

    def getAllProcessInfo(self):
        return self.s.supervisor.getAllProcessInfo()


def get_socket_path(supervisor_conf=DEFAULT_SUPERVISOR_CONF):
    conf = supervisor_conf or '/etc/supervisord.conf'
    parser = ConfigParser.ConfigParser()
    parser.read(conf)
    socket_path = parser.get('supervisorctl','serverurl')
    return socket_path

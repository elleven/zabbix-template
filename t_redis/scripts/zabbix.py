import subprocess
from config import HOST, ZABBIX_SERVER 

def push_to_zabbix(key, value):
    subprocess.Popen("/usr/local/zabbix/bin/zabbix_sender -k %s -z %s -s %s -o '%s' >/dev/null 2>&1" % (key, ZABBIX_SERVER, HOST, value), shell=True)
    #print "zabbix_sender -k %s -z %s -s %s -o '%s' >/dev/null 2>&1" % (key, ZABBIX_SERVER, HOST, value)

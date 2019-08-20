import subprocess
from config import HOST, ZABBIX_SERVER



def push_to_zabbix_by_shell(key, value):
    subprocess.call("zabbix_sender -k %s -z %s -s %s -o '%s' >/dev/null" % (key, ZABBIX_SERVER, HOST, value), shell=True)



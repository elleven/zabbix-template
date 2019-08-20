import socket

ZABBIX_SERVER = 'zabbix.tigerbrokers.net'
HOST = socket.gethostname()

DEFAULT_SUPERVISOR_CONF='/etc/supervisord.conf'
DISCOVERY_INTERVAL = 3600
PAUSE_AFTER_PUSH = 60


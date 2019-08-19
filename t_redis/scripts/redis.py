import config
import subprocess

class redis(object):
    def __init__(self, conf):
        with open(conf) as fr:
            for line in fr:
                if line.startswith('port'):
                    self.port = line.split()[1].rstrip() 
                
                if line.startswith('requirepass'):
                    self.requirepass = line.split()[1].rstrip()
                if line.startswith('bind'):
                    self.host = line.split()[1].rstrip()

        if 'port' not in self.__dict__:
            self.port = 6379

        if 'requirepass' not in self.__dict__:
            self.requirepass = ''
        if 'host' not in self.__dict__:
            self.host = '127.0.0.1'

        self.info = redis_info(self.host, self.port, self.requirepass)
        self.latest_slowlog = redis_latest_slowlog(self.host, self.port, self.requirepass)
        self.config = redis_config(self.host, self.port, self.requirepass)
    
    @classmethod
    def parse_info(cls, response):
        info = {}
        def get_value(value):
            if ',' not in value or '=' not in value:
                try:
                    if '.' in value:
                        return float(value)
                    else:
                        return int(value)
                except ValueError:
                    return value
            else:
                sub_dict = {}
                for item in value.split(','):
                    k, v = item.rsplit('=', 1)
                    sub_dict[k] = get_value(v)
                return sub_dict
    
        for line in response.splitlines():
            if line:
                if line.startswith('#'):
                    section = line.split()[-1] 
                    info[section] = {}
                else:
                    if line.find(':') != -1:
                        key, value = line.split(':', 1)
                        info[section][key] = get_value(value)
                    else:
                        # if the line isn't splittable, append it to the "__raw__" key
                        info[section].setdefault('__raw__', []).append(line)
    
        return info

class redis_config(object):
    def __init__(self,host, port, requirepass):
        d = subprocess.Popen([ '{0} -p {1} -a "{2}" -h {3} config get "*"'.format(config.REDIS_CLI, port, requirepass,host) ], shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
        self.__dict__.update(zip(d[0::2], d[1::2]))
    
class redis_info(object):
    def __init__(self, host,port, requirepass):
        self.__dict__.update(redis.parse_info(subprocess.Popen([ '{0} -p {1} -a "{2}" -h {3} info'.format(config.REDIS_CLI, port, requirepass,host) ], shell=True, stdout=subprocess.PIPE).communicate()[0]))

class redis_latest_slowlog(object):
    def __init__(self,host, port, requirepass):
        response = subprocess.Popen([ '{0} -p {1} -a "{2}" -h {3} slowlog get 1'.format(config.REDIS_CLI, port, requirepass,host) ], shell=True, stdout=subprocess.PIPE).communicate()[0].rstrip().splitlines()
        if response:
            self.id = response[0]
            self.start_time = response[1]
            self.duration = response[2]
            self.command = " ".join(response[3:])

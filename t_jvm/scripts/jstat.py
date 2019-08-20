import subprocess
from exception import PIDNOTExistException

# if need use "su - user -c 'jstat -gc {vmid}'"
class JSTAT_GC(object):
    def __init__(self, vmid):
        p_jstat = subprocess.Popen([ 'jstat -gc {vmid}'.format(vmid=vmid) ], shell=True, stdout=subprocess.PIPE)
        p_output = p_jstat.communicate()[0]
        if p_jstat.returncode != 0:
            raise Exception('jstat return code not zero')

        headers, stats = p_output.splitlines()
        self.gc = {}
        index = 0
        stats = stats.split()
        for header in headers.split():
            try:
                value = float(stats[index]) 
            except ValueError:
                pass

            self.gc[header] = value

            index += 1

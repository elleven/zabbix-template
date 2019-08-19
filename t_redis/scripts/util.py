import time

def cpu(pid, processor_num, sample_interval=1):
    def get_total():
        with open('/proc/stat') as fr:
            for line in fr:
                if line.startswith('cpu'):
                    return sum([ int(field) for field in line.split()[1:] ])
    def get_proc(pid):
        with open('/proc/{0}/stat'.format(pid)) as fr:
           stats = fr.read().split()
           return sum([ int(field) for field in stats[13:17] ])

    prev_total = get_total()
    prev_proc = get_proc(pid)

    time.sleep(sample_interval)

    return processor_num * (float(get_proc(pid) - prev_proc)/(get_total() - prev_total)) * 100

def get_processor_num():
    return len([ line for line in open('/proc/cpuinfo') if line.startswith('processor') ])

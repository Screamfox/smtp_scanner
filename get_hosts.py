#!/usr/bin/python3

import socket, re
import itertools, sys, os
import multiprocessing

##### get_hosts
### v0.2
# GOALS:
#   [/] refactor the v0.1 code
#   [ ] launch a process every t nseconds 
#   [x] allow only n calls to be made in parralel
#(  [ ] find better way of obtaining the hostname of an IP)
#   [x] make pweety print part more convinient (stop repeating yourself)

### v.0.1.0
# GOALS:
#	[x] read the ipz list
#	[x] get hostnames
#   [x] filter the domains against hostname pattern

print("BOP")

# a way to pweety print stuff
print('%-24s%-48s%-24s%-8s' % ("IP", "DNS", "DOMAIN", "RESPONSE"))

def val_to_text(val):
    if val == -1:   return "FAIL"
    elif val == 0:  return "OK"
    elif val == 1:  return "UNCHANGED"

# socket.getfqdn is just socket.gethostbyname, but returns the best dns as string
def get_dns(ip):
    if socket.getfqdn(ip) != ip: return socket.getfqdn(ip)
    else:                        return "FAIL"

###	This pattern detects links and breaks the down in regexp groups.
# eg. from domain.co.uk
# group(4) => `domain_name`
# group(5) => `co`
# group(9) => `.uk`
pattern = re.compile("((www\.)|([a-z0-9_\-]{1,}\.)+)?([a-z0-9_\-]{3,})\.([a-z]{2,4})(\/([a-z0-9_\-]{1,}\/)+)?([a-z0-9_\-]{1,})?(\.[a-z]{2,})?(\?)?(((\&)?[a-z0-9_\-]{1,}(\=[a-z0-9_\-]{1,})?)+)?")
def get_hostname(dns):
    match = re.search(pattern, dns)
    if match:
        hostname = match.group(4) + "." + match.group(5)
        # Add the second domain to hostname if the hostname has a double dot domain ending e.g. "domain.co.uk"
        hostname = hostname + match.group(9) if str(match.group(9)) != 'None' else hostname
        return hostname
    else: return "FAIL"

# I thought of testing the hostnames by 
# pinging the hostname on port 587 ... what could go wrong ? 
# hping requires _sudo_ rights to be run.
def ping(hostname, hping=False):
    if hping:
        try: response = os.system("sudo hping3 --faster -c 1 -S -p 587 " + hostname + " > /dev/null 2>&1")
        except: print("hping is not installed !"); sys.exit()
    else: response = os.system("ping -c 1 -w2 " + hostname + " > /dev/null 2>&1")

    if response == 0: return  0
    else:             return -1

class process:
    def __init__(self, ip):
        self.ip = ip
        self.dns = "FAIL"
        self.hostname = "FAIL"
        self.response = 1
    
    def start(self):
        self.dns = get_dns(self.ip)
        if self.dns != "FAIL":       self.hostname = get_hostname(self.dns)
        else:                        return -1

        if self.hostname != "FAIL":  self.response = ping(self.hostname)
        else:                        return -1
        
        print('%-24s%-48s%-24s%-8s' % (self.ip, self.dns, self.hostname, val_to_text(self.response)))
        return self.response

class controller:
    def __init__(self, queueLimit = 10):
        self.queueLimit = queueLimit
        self.QUEUE = []

    # TODO(kid): Check if an IP already exists / has existed.
    def start_process(self, process):
        if (len(self.QUEUE)) >= self.queueLimit:
            return -1
        else:
            self.QUEUE.append(process)
            if process.start(): self.QUEUE.remove(process)

# TODO(kid): If not used, just remove
def get_ips_as_array(filename):
    OUTPUT = []
    with open(filename) as f:
        for line in f:
            line = line.strip() # strip ≜ trim
            OUTPUT.append(line)
    return OUTPUT

def write_output(filename, string):
    output = open(filename, "a+")
    ouput.write(string + "\n")
    output.close()

def multi_processing(function, array, processes = 4):
    if __name__ == '__main__':
        p = multiprocessing.Pool(processes)
        p.map(function, array)

# TODO(kid):
#   IP Array is broken down into p parts, where p is the number of processes
#   Every process spawns a class which takes a part of all IPS
#
#   FOR EVERY PROCESS:
#   send IP => controller
#   controller responds
#   if  0: delete last IP from list, sleep, send next IP
#   if -1: sleep, retry to send last IP

print("EOP")
#!/usr/bin/python3

import socket, re
import itertools, sys, os
import multiprocessing

##### get_hosts
### v0.2
# TODO(kid): TEST yo' shit
# GOALS:
#   [x] refactor the v0.1 code
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

def split_array(array, parts = 1):
    length = len(array)
    return [ array[i*length // parts: (i+1)*length // parts] 
             for i in range(parts) ]

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
    def __init__(self):
        self.IPZ = []
        self.RESULTS = {}
    
    def start(self):
        for ip in self.IPZ:
            dns = get_dns(ip)
            
            if dns != "FAIL":           hostname = get_hostname(dns)
            else:                       hostname = "FAIL"; response = "FAIL"

            if hostname != "FAIL":      response = ping(hostname)
            else:                       response = "FAIL"

            print('%-24s%-48s%-24s%-8s' % (self.ip, self.dns, self.hostname, val_to_text(self.response)))

            if response == "FAIL":      continue
            else:                       self.RESULTS[ip] = hostname
        
        return 0

    def write_results(self, filename):
        for key in self.RESULTS.keys():
            write_output(filename, key + " " + self.RESULTS[key])

class container:
    def __init__(self, process_limit = 10):
        self.ips_array = []
        self.process_limit = process_limit
        self.PROCESSES = []
    
    def add_ips(self, filename):    self.ips_array = get_ips_as_array(filename)
    def add_process(self, p):       self.PROCESSES.append(p)
    def n_of_ps(self):              return len(self.PROCESSES)

    def divide_ips(self):
        arrays = split_array(self.ips_array, n_of_ps())
        
        i = 0
        for p in self.PROCESSES:
            p.IPZ = arrays[i]
            i += 1
    
    def start_all_ps(self):
        for p in self.PROCESSES:
            p.start()




def get_ips_as_array(filename):
    OUTPUT = []
    try: File = open(filename, "r+")
    except:
        print("")

    with File as f:
        for line in f:
            line = line.strip() # strip ≜ trim
            OUTPUT.append(line)
    return OUTPUT

def write_output(filename, string):
    try: output = open(filename, "a+")
    except:
        print(filename + " does not exist.")
        sys.exit()
    
    ouput.write(string + "\n")
    output.close()

print("EOP")
# Import modules
import re
import sys
import time



# Set variables
#iplist = {}
logfile = sys.argv[1]
#outputfile = "/app/output.txt"

# Read and parse /var/log/auth.log file in container fetching timestamps and ip addresses attempting to login to SSH daemon

def get_ip_time():
    while True:
        with open(logfile, 'r') as f:
            for line in f:
                ip = (re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line))
                timestamp = line[0:15]
                return timestamp, ip
        time.sleep(10)
        continue
get_ip_time()
import re
import sys

iplist = {}
logfile = sys.argv[1]

with open(logfile, 'r') as f:
    for line in f:
        ip = (re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line))
        timestamp = line[0:15]
        iplist.update({str(timestamp):str(ip)[2:-2]})
    print(iplist)

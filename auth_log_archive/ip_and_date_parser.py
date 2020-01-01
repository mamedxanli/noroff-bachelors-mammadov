import re
import sys

iplist = []
logfile = sys.argv[1]

with open(logfile, 'r') as f:
    for line in f:
        ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
        if ip not in iplist:
            iplist.append(ip)
    print(iplist)

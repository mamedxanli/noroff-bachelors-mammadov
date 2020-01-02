import re
import sys
import time




iplist = {}
logfile = sys.argv[1]
outputfile = "/app/output.txt"

while True:
    with open(logfile, 'r') as f:
        for line in f:
            ip = (re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line))
            timestamp = line[0:15]
            iplist.update({str(timestamp):str(ip)[2:-2]})
        #rint(iplist)
        with open(outputfile, 'w') as o:
            o.write(str(iplist))
    time.sleep(10)
    continue

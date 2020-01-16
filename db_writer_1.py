import socket
import zlib
import xml.sax
import time
import struct
import xml.etree.ElementTree as ET
from cStringIO import StringIO
from influxdb import client as influxdb


MCGRP = "230.0.0.2"
MCPORT = 34960

dblist = list()
dbname = "lucy_linus_source_id"

db1 = influxdb.InfluxDBClient('10.0.1.133', '8086', 'root', 'root', dbname)
db2 = influxdb.InfluxDBClient('10.0.1.134', '8086', 'root', 'root', dbname)
db3 = influxdb.InfluxDBClient('10.0.3.158', '8086', 'root', 'root', dbname)

dblist.append(db1)
dblist.append(db2)
dblist.append(db3)

def buildQuery(epoch, nccmach, nccinst, nccloc, g4svc, g4src):
    convtm = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(float(epoch)))
    data = {
        "measurement"  : "Lucy",
        "tags"         : {
            "lucy_machine"  : nccmach,
            "lucy_location" : nccloc,
            "lucy_location" : nccloc,
            "lucy_service"  : g4svc,
        },
        "time"     : convtm,
        "fields"   :     {
            "lucy_source"   : float(g4src),
        }
    }
    return data


def connect(MCGRP, MCPORT, dblist):

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((MCGRP, MCPORT))
            mreq = struct.pack("4sl", socket.inet_aton(MCGRP), socket.INADDR_ANY)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            data = s.recv(4096)
            stream = zlib.decompress(data)
            f = StringIO(stream)
            tree = ET.parse(f)
            root = tree.getroot()
            datadict = {}
            included_tags = ["source", "service", "time", "machine", "id", "location"]
            if "orbitClockSource" in root.tag:
                for child in root:
                    if child.tag in included_tags:
                       #print child.tag,child.text
                       datadict[child.tag] = child.text
                       for k,v in child.attrib.items():
                           #print k,v
                           datadict[k] = v
                if datadict["service"] == "3":
                    new_data = buildQuery(datadict["time"], datadict["machine"],
                        datadict["instance"], datadict["location"], datadict["service"], datadict["source"])
                    #print(new_data)
                    for db in dblist:
                        db.write_points([new_data])
            continue
        except socket.error as e:
            print("error: %s" % e)
            time.sleep(5)

connect(MCGRP, MCPORT, dblist)
import time
from datetime
from cStringIO import StringIO
from influxdb import client as influxdb
import re
import sys

logfile = sys.argv[1]


#TODO: 
#1. write convert_time function
#2. finish influx tcp structure builder

def convert_time(timestamp):
    try:
        # Add .0 in case that the epoch didn't include it
        if "." not in timestamp:
            timestamp = timestamp + ".0"
        epoch = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        return epoch
    except Exception as exc:
        raise ValueError(f"Exception while building influx tcp structure, transforming the epoch passed into datetime: {exc}.\nUse format: 2019-03-20T00:08:44.883722\n")
    

def get_ip_epoch(logfile):
    #reads logfile, parses it and returns epoch and ip
    with open(logfile, 'r') as f:
        for line in f:
            ip = (re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line))
            timestamp = line[0:15]
            epoch = convert_time(timestamp)
            return epoch, ip

def geolocator(ip):
    #gets ip address and returns geohash, country, city
    pass


def build_influx_tcp_structure(measurement: str, epoch: str, tags: dict = {}, fields: dict = {}) -> dict:
    """
    Builds data structure for Influx. To be used in the TCP port localhost:8086.\n
    This port is the InfluxDB Docker container running.
    If no epoch is passed, defaults to datetime.now().\n
    Expects:\n
        - measurement: Main value to search in Grafana. (similar to Table name)
        - value: The value of said measurement. Defaults to float 1. Unless the measurement is really simple with no relation to "fields", leave it at default.
        - epoch: Timestamp of the measurement. Format is 2019-03-20T00:08:44
        - fields: Optional: Dict if more fields want to be stored. Fields can contain values, like cpu usage, temperature, or traffic. Usually used with numeric values for plot.
        - tags: Optional: Dict with tags for this measurement. Tags can be used as identifiers or labels. Usually strings to sort data by groups.
    """
    try:
        # value goes into fields, more like a placeholder
        fields["value"] = float(value)
        # Main dictionary
        data = {
            "measurement" : measurement,
            "time" : epoch,
            "ip"   : ip,
        }
        # Nest dictionaries
        data["tags"] = tags
        data["fields"] = fields
        fields = {
            "country" : country,
            "city" : city,
            "geohash" : geohash,
        }
        #print(data) # Debug
        print(data)
        return data
    except Exception as exc:
        raise ValueError(f"Exception while building influx tcp structure: {exc}.")

def db_writer(data):
    dbname = "honeypot"
    db = influxdb.InfluxDBClient('influx', '8086', 'root', 'root', dbname)
    while True:
        try:
            new_data = buildQuery(data["measurement"], datadict["epoch"],
            datadict["value"], datadict["tags"], datadict["fields"])
            db.write_points([new_data])
            continue
        except Exception as exc:
            raise ValueError(f"Exception while building influx tcp structure: {exc}.")
            time.sleep(5)

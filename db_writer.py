import time
from datetime import datetime
from influxdb import client as influxdb
import re
import sys
import json
import geoip
from contextlib import suppress
import geohash

logfile = '/var/log/auth.log'
dbname = 'honeypot'
measurement = 'ssh_honeypot'

def get_geolocation(ip):
        try:
            data = geoip.geolite2.lookup(ip)
            if data:
                return data.to_dict()
            return {}            
        except Exception as exc:
            raise ValueError(f"Exception while building influx tcp structure: {exc}.")

def parser(logfile):
    regex_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    #regex_value = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    all_lines_processed = list()
    with open(logfile, 'r') as f:
        for line in f:
            if re.findall(regex_pattern, line) == []:
                continue
            else:
                tags_dict = {}
                fields_dict = {}
                ip = str(re.findall(regex_pattern, line))[2:-2]
                geodata = get_geolocation(ip)
                if geodata:
                    epoch = line[0:26]
                    continent = geodata['continent']
                    country = geodata['country']
                    location = geodata['location']
                    latlong = [x.strip() for x in str(location).split(',')]
                    latitude = latlong[0]
                    longitude = latlong[1]
                    geohash_data = geohash.encode(float(latitude[1:]), float(longitude[:0-1]))
                    fields_dict["ip"] = ip
                    tags_dict["continent"] = continent
                    tags_dict["country"] = country
                    fields_dict["latitude"] = latitude[1:]
                    fields_dict["longitude"] = longitude[:-1]
                    fields_dict["geohash_data"] = geohash_data
                    ready_influx_structure = build_influx_tcp_structure(epoch=epoch, tags=tags_dict, fields=fields_dict)
                    all_lines_processed.append(ready_influx_structure)
        return all_lines_processed
def build_influx_tcp_structure(epoch: str, measurement: str = "ssh_honeypot", value: float = 1.0, tags: dict = {}, fields: dict = {}) -> dict:
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
        }
        # Nest dictionaries
        data["tags"] = tags
        data["fields"] = fields
        #print("output from influx builder: ", data) # Debug
        return data
    except Exception as exc:
        raise ValueError(f"Exception while building influx tcp structure: {exc}.")



def write_to_db(data):
    print("checking if writer gets data: ", data)
    db_connection = influxdb.InfluxDBClient('influx', '8086', 'admin', 'admin123', dbname)
    try:
        db_connection.write_points(data)
        #continue
    except Exception as exc:
        raise InfluxDBClientError(f"Exception while writing to db: {exc}.")


#if __name__ ==' __main__':
influx_data = parser(logfile)
write_to_db(influx_data)


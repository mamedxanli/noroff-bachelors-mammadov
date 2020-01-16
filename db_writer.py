import time
from datetime import datetime
from influxdb import client as influxdb
import re
import sys
import json
import geoip
from contextlib import suppress
import geohash

logfile = sys.argv[1]
dbname = sys.argv[2]
measurement = sys.argv[3]

#TODO: 
#2. finish influx tcp structure builder

{'ip': '8.8.8.8', 'hostname': 'dns.google', 'city': 'Mountain View', 'region': 'California', 'country': 'US', 'loc': '37.3860,-122.0838', 'org': 'AS15169 Google LLC', 'postal': '94035', 'timezone': 'America/Los_Angeles', 'readme': 'https://ipinfo.io/missingauth'}

def get_geolocation(ip):
    data = geoip.geolite2.lookup(ip)
    return data.to_dict()


def process_input_data(logfile):
    regex_value = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    #reads logfile, parses it and returns epoch, ip, continent, country, location and geohash
    with open(logfile, 'r') as f:
        for line in f:
            with suppress(Exception):
                try:
                    ip = str((re.findall(regex_value, line)))
                    epoch = line[0:26]
                    geodata = get_geolocation(ip[2:-2])
                    continent = geodata['continent']
                    country = geodata['country']
                    location = geodata['location']
                    latlong = [x.strip() for x in str(location).split(',')]
                    latitude = latlong[0]
                    longitude = latlong[1]
                    geohash_data = geohash.encode(float(latitude[1:]), float(longitude[:0-1]))
                    print(epoch, ip, continent, country, location, geohash_data)
                    return epoch, ip, continent, country, location, geohash_data
                except Exception as exc:
                    raise ValueError(f"Exception while getting geodata: {exc}.")

def build_influx_tcp_structure(logfile, measurement: str, epoch: str, tags: dict = {}, fields: dict = {}) -> dict:
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
            "continent" : continent,
            "country" : country,
            "location" : location,
            "geohash_data" : geohash_data
        }
        # Nest dictionaries
        data["tags"] = tags
        data["fields"] = fields
        fields = {
            "country" : country,
            "location" : location,
            "geohash_data" : geohash_data,
        }
        #print(data) # Debug
        return data
    except Exception as exc:
        raise ValueError(f"Exception while building influx tcp structure: {exc}.")

def db_writer(logfile, dbname, measurement):
    db_connection = influxdb.InfluxDBClient('influx', '8086', 'admin', 'admin123', dbname)
    #epoch, ip, continent, country, location, geohash_data = process_input_data(logfile)
    while True:
        try:
            new_data = build_influx_tcp_structure(logfile, measurement)
            db_connection.write_points([new_data])
            continue
        except Exception as exc:
            raise ValueError(f"Exception while building influx tcp structure: {exc}.")
            time.sleep(5)

if __name__ == '__main__':
    db_writer(logfile, dbname, measurement)

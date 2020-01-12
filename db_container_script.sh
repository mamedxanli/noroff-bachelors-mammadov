#!/bin/bash

apt update
apt install procps
apt install vim

#commands for influxdb
influx
$ sudo vi /etc/influxdb/influxdb.conf

[http]
  # Determines whether HTTP endpoint is enabled.
  enabled = true
  
  # The bind address used by the HTTP service.
  bind-address = ":8086"

sudo systemctl restart influxdb

CREATE DATABASE "honeypot" WITH DURATION 365d

# Python script
from influxdb import InfluxDBClient
from influxdb import SeriesHelper

# InfluxDB connections settings
host = 'localhost'
port = 8086
user = 'root'
password = 'root'
dbname = 'mydb'

myclient = InfluxDBClient(host, port, user, password, dbname)
influx -database 'honeypot' -execute 'alter retention policy autogen on honeypot duration 5d'


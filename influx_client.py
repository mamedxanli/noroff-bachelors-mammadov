#1. Honeypot machine container starts parsing data.

#2. python script 



from influxbd import InfluxDBClient
host = "noroffbachelorsmammadov_db_1"
port = 8086
dbname = "honeypot"

client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
client.create_database(DBNAME)



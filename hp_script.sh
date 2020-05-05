# Start ssh service
service ssh start
# Enable port 22 for SSH daemon to listen
echo "Port 22" >> /etc/ssh/sshd_config
# Enable all address families ipv4 and ipv6
echo "AddressFamily any" >> /etc/ssh/sshd_config
# Listen for all ip addresses
echo "ListenAddress 0.0.0.0" >> /etc/ssh/sshd_config
# Enable SSH logging to /var/log/auth.log
echo "SyslogFacility AUTH" >> /etc/ssh/sshd_config
# Set logging level INFO
echo "LogLevel INFO" >> /etc/ssh/sshd_config
# Enable root account login on SSH daemon
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
# Set maximum authentication tries to 3 attempts
echo "MaxAuthTries 3" >> /etc/ssh/sshd_config
# Restart SSH daemon
service ssh restart
#Change Rsyslog timestamp formatting from traditional to high precise
sed -i "/$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat/c\$ActionFileDefaultTemplate RSYSLOG_FileFormat" /etc/rsyslog.conf
# Start Rsyslog daemon
service rsyslog start
# Set auth.log file location
LOGFILE=/var/log/auth.log
# Set output file for Python parser script ip_and_date_parser.py reading atuh.log file and fetching data of interest
OUTPUTFILE=/app/output.txt
# Rename Geohash module folder - looks like its buggy and doesnt work with original name
mv /usr/local/lib/python3.6/dist-packages/Geohash /usr/local/lib/python3.6/dist-packages/geohash
# Fix __init__.py content for geohash module, adding .geohash instead of geohash:
sed -i "/from geohash import decode_exactly, decode, encode/c\from .geohash import decode_exactly, decode, encode" /usr/local/lib/python3.6/dist-packages/geohash/__init__.py 
#Create /var/log/auth.log file and set permissions
touch /var/log/auth.log
chown syslog:adm /var/log/auth.log 
# start infinite loop
while true
    do
        # if auth.log file exists
        if [ -e $LOGFILE ]; then
            # run parser script
            python3 db_writer.py
        else
        # otherwise print out in console
        echo "$LOGFILE does not exist"
        fi
    # reset the content of auth.log file and wait 10 seconds
    echo "resetting the content" > /var/log/auth.log
    sleep 10
    done

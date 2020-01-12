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
# Start Rsyslog daemon
service rsyslog start
# Set auth.log file location
LOGFILE=/var/log/auth.log
# Set output file for Python parser script ip_and_date_parser.py reading atuh.log file and fetching data of interest
OUTPUTFILE=/app/output.txt
# start infinite loop
while true
    do
        # if auth.log file exists
        if [ -e $LOGFILE ]; then
            # run parser script
            python3 ip_and_date_parser.py /var/log/auth.log
        else
        # otherwise print out in console
        echo "$LOGFILE does not exist"
        fi
    # wait 10 seconds
    sleep 10
    done

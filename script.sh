service ssh start
echo "Port 22" >> /etc/ssh/sshd_config
echo "AddressFamily any" >> /etc/ssh/sshd_config
echo "ListenAddress 0.0.0.0" >> /etc/ssh/sshd_config
echo "SyslogFacility AUTH" >> /etc/ssh/sshd_config
echo "LogLevel INFO" >> /etc/ssh/sshd_config
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
echo "MaxAuthTries 3" >> /etc/ssh/sshd_config
service ssh restart
service rsyslog start
LOGFILE=/var/log/auth.log
OUTPUTFILE=/app/output.txt
while true
    do
        if [ -e $LOGFILE ]; then
            python3 ip_and_date_parser.py /var/log/auth.log
        else
        echo "$LOGFILE does not exist"
        fi
    sleep 10
    echo `cat $OUTPUTFILE`
    done

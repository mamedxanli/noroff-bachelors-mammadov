# noroff-bachelors-mammadov

In order to build the solution, it was decided to use the following components:
- Cisco ASA firewall 5510 with Internet connection and static public ip address.
- Cisco Catalyst switch WS-C3560-PS for LAN services.
- Lenovo laptop used as a server and host for Docker containers.
- Ubuntu 16.04 as host OS.
- docker version 19.03.1
- docker-compose version 1.12.0
- ubuntu latest docker build
- install necessary software through docker-compose and Dockerfile
- run entry point script (for now its software installation and ping to make the container run)
- in the future entry point script is going to run python solution to fetch the data from auth.log and dump it in a Sqlite db.

after:
edit etc/ssh/sshd_config for port, Root login, log files

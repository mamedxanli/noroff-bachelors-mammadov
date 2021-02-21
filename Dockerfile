# Use an official Python runtime as a parent image
FROM ubuntu:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Installing dependencies and specified software
RUN apt-get update
RUN apt-get install -y net-tools 
RUN apt-get install -y iputils-ping
RUN apt-get install -y ssh
RUN apt-get install -y vim
RUN apt-get install -y rsyslog
RUN apt-get install -y python3-pip

# Installing software specified in the file
RUN pip3 install -r requirements.txt

# Exposing port 2222 to outside networks
EXPOSE 2222

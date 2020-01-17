# Use an official Python runtime as a parent image
FROM ubuntu:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Installing dependencies and required software
RUN apt-get update && apt-get install -y net-tools && apt-get install -y iputils-ping && apt-get install -y ssh && apt-get install -y vim && apt-get install -y rsyslog && apt-get install -y sqlite3 && apt-get install -y python3-pip

RUN pip3 install -r requiremets.txt

# Exposing port 2222 to outside networks
EXPOSE 2222

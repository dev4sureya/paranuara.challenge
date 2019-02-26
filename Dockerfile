################################################################################
# Filename    : Dockerfile
# Description : This Dockerfile contains the Docker builder commands for Flask app
# Developer   : Suresh Kumar
# Date        : 26th Feb 2019
################################################################################
FROM python:3.6.3

MAINTAINER Suresh Kumar

# install the python requirements
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt 

## run the app 
ADD app.py app.py
ADD datamodel.py datamodel.py
ADD people.json people.json
ADD companies.json companies.json
ADD fruits_vegetables.json fruits_vegetables.json

## expose the port
EXPOSE 5000

## start the command
CMD ["python", "app.py"]

# py-ecobee-mqtt

Python script to push Ecobee thermostat information (set points, remote sensors, settings, etc) to my local mqtt

# Setup
## Config File

Modify *config.cfg.example* and rename as *config.cfg*.  Include the following parameters:

	[mqtt]
	ipaddr = 'yourMqttServerIP'
	port = 1883
	topic = 'yourMqtt/tokenName/here'

	[ecobee]
	token = 'yourTokenHere'
	thermostatname = 'My ecobee'
Mqtt parameters should be self explanatory, Ecobee token comes from ecobee.com, you must enable Developer mode and add your token.  Unsure if thermostatname is required, but I used it.

This file is copied into the docker container on build, so it is required to be configured.

## Testing Python Script locally

Temporarily create two local folders 'db' and 'log' for the script to store files in (**todo: add this mkfile to script when run locally?**)

After updating config.cfg file, run the *py-ecobee-mqtt.py* script

    python py-ecobee.mqtt.py

On first run you will need to authorize app with ecobee.com in the My Apps section. Follow instructions, this will make a persistent database file in ./db folder created above.

# Docker
I did this development on a Windows machine in Git Bash, so a couple of these commands might be a little wonky...
## Build the docker file

    docker build -t py-ecobee-mqtt .

Response:

    Sending build context to Docker daemon  393.2kB
	Step 1/8 : FROM python:3.8
	 ---> 6feb119dd186
	Step 2/8 : copy config.cfg /app/config.cfg
	 ---> Using cache
	 ---> 3ee55f1d1ac9
	Step 3/8 : copy py-ecobee-mqtt.py /app/py-ecobee-mqtt.py
	 ---> Using cache
	 ---> 123195343b41
	Step 4/8 : copy requirements.txt /app/requirements.txt
	 ---> Using cache
	 ---> 290e37fd0bb4
	Step 5/8 : RUN mkdir /app/db
	 ---> Using cache
	 ---> 3c2cc1eacbba
	Step 6/8 : RUN mkdir /app/log
	 ---> Using cache
	 ---> 784bdda8a8ee
	Step 7/8 : RUN pip install -r /app/requirements.txt
	 ---> Using cache
	 ---> b9ca4fdef638
	Step 8/8 : CMD ["python", "/app/py-ecobee-mqtt.py"]
	 ---> Using cache
	 ---> bb4917475693
	Successfully built bb4917475693
	Successfully tagged py-ecobee-mqtt:latest
	SECURITY WARNING: You are building a Docker image from Windows against a non-Windows Docker host. All files and directories added to build context will have '-rwxr-xr-x' permissions. It is recommended to double check and reset permissions for sensitive files and directories.




## First time executing!
You can either copy the *pyecobee_db* file created (and authorized) previously into your mapped -v db directory, or else use '-it' command below to reauthorize app
### Interactive authorization

     winpty docker run -it -v "C:\Users\derek.ROWKAR\Documents\repos\py-ecobee-mqtt\log-docker":/app/log -v "C:\Users\derek.ROWKAR\Documents\repos\py-ecobee-mqtt\db-docker":/app/db -name py-ecobee-mqtt py-ecobee-mqtt
winpty - Git Bash isn't a tty client, so can't use interactive mode, winpty lets us interact with docker run command

 - *winpty* : Git Bash isn't a tty client, so can't use interactive mode,
   winpty lets us interact with docker run command
 - *docker run -it* : run the docker container in interactive and tty modes so we can authorize app if needed
 - *-v [local folder]:/app/log* : maps docker's log folder to a folder on your local PC so you can checkout logs
 - *-v [local folder]:/app/db* : maps docker's db folder to local PC so it stays authorized with ecobee.com persistently
 - *py-ecobee-mqtt* : this is the name of the container built above
 
To exit, hit CTRL+C and container should continue running

### Run detached

Add "-d" to command above once it's running

     winpty docker run -it -v "C:\Users\derek.ROWKAR\Documents\repos\py-ecobee-mqtt\log-docker":/app/log -v "C:\Users\derek.ROWKAR\Documents\repos\py-ecobee-mqtt\db-docker":/app/db -d -name py-ecobee-mqtt py-ecobee-mqtt

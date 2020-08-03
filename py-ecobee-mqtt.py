#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    File name: py-ecobee-mqtt.py
    Author: Derek Rowland
    Date created: 2020/08/03
    Date last modified: 2020/08/03
    Python Version: 3.8.5
'''

'''
******* Imports 
'''
import requests
import os
from configparser import ConfigParser
import paho.mqtt.client as mqtt


'''
******* Header Vars
'''

__author__ = "Derek Rowland"
__copyright__ = "Copyright 2020"
__credits__ = ["Derek Rowland"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Derek Rowland"
__email__ = "gx1400@gmail.com"
__status__ = "Development"

'''
******* Global vars
'''
mqttAddr = 'not loaded'
mqttPort = -1
mqttTopic = 'not loaded'
tokenEcobee = 'not loaded'

'''
******* Functions
'''
def main():
    # Read Config File parameters
    readConfig()

    # Connect to Ecobee and Create 
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(mqttAddr + ':' + str(mqttPort))

    client.connect(mqttAddr, mqttPort, 60)
    #client.connect('10.10.10.41', 1883, 60)

    client.loop_forever()

# call back for client connection to mqtt
def on_connect(client, userdata, flags, rc):
    print('Connected with result code: ' + str(rc))

    # subscribing in on_connect means if we lose the connection and 
    # reconnect then subscriptions will be renewed
    client.subscribe('$SYS/#')

# call back for when a public message is received by the server
def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))


def readConfig():
    parser = ConfigParser()
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    configfile = os.path.join(thisfolder, 'config.cfg')
    parser.read(configfile, encoding=None)

    global mqttAddr, mqttPort, mqttTopic, tokenEcobee

    mqttAddr = parser.get('mqtt', 'ipaddr')
    mqttPort = parser.getint('mqtt', 'port')
    mqttTopic = parser.get('mqtt', 'topic')

    tokenEcobee = parser.get('ecobee', 'token')

if __name__ == "__main__":
    main()
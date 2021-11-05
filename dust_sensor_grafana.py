import time
import RPi.GPIO as GPIO
import requests, json
from influxdb import InfluxDBClient as influxdb
import serial

client = None

# arduino
port = '/dev/ttyACM0'
brate = 9600
cmd = 'temp'
a = 1
while (True):

    if client is None:
        try:
            client = influxdb('localhost', 8086,'root','root', 'dust')
        except Exception as e:
            print("Exception", str(e))

    seri = serial.Serial(port, baudrate = brate, timeout = None)
    seri.write(cmd.encode())

    time.sleep(1)
    if client is not None:
        try:
            if seri.in_waiting != 0:
                content = seri.readline().decode()
                content = int(content[:content.find('.')])
                print(content)
                #a = content;
                data = [{
                    'measurement' : 'dust',
                    'tags':{
                        'Uni' : 'inhatc',
                    },
                    'fields': {
                        'dust': content,
                    }
                }]
                client.write_points(data)
        except Exception as e:
            print("Exception write ",str(e))
        finally:
            client.close()
    print ("running influx ok")

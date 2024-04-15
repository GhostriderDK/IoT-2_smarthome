from get_data import *
import paho.mqtt.publish as publish
from time import sleep

def fan():
    timestamps, temp, hum, tvoc, part, co2 = get_stue_data(1)
    print('temp: ' + str(temp[0]))
    print('hum: ' + str(hum[0]))
    print('co2: ' + str(co2[0]))
    
    if hum[0] > 50:
        publish.single("sensor/stue/fan", "1", hostname="localhost")
   
    elif co2[0] > 1100:
        publish.single("sensor/stue/fan", "1", hostname="localhost")

    elif co2[0] < 700:
        publish.single("sensor/stue/fan", "0", hostname="localhost")

    elif hum[0] < 30:
        publish.single("sensor/stue/fan", "0", hostname="localhost")

print('fan script running')
while True:
    fan()
    sleep(10)
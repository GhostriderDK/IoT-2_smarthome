from get_data import *
import paho.mqtt.publish as publish
from time import sleep

def fan():
    timestamps, temp, hum, tvoc, part, co2 = get_stue_data(1)
    print('temp: ' + temp[0])
    print('hum: ' + hum[0])
    print('co2: ' + co2[0])
    if temp[0] > 25 and hum[0] > 50:
        publish.single("sensor/stue/fan", "1", hostname="localhost")
   
    elif temp[0] > 25 and co2[0] > 1100:
        publish.single("sensor/stue/fan", "1", hostname="localhost")

    elif temp[0] < 18 and co2 < 500:
        publish.single("sensor/stue/fan", "0", hostname="localhost")

    elif temp[0] < 18 and hum[0] < 30:
        publish.single("sensor/stue/fan", "0", hostname="localhost")

print('fan script running')
while True:
    fan()
    sleep(1)
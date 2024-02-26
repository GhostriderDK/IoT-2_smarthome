import paho.mqtt.publish as publish
import json
import Adafruit_DHT


sensor = Adafruit_DHT.DHT11
pin = 4

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        payload = {
            "temperature" : temperature,
            "humidity" : humidity,

        }
        publish.single("paho/test/topic", json.dumps(payload), hostname="74.234.16.65")
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        
    

# pip install paho-mqtt
# pip install Adafruit-DHT
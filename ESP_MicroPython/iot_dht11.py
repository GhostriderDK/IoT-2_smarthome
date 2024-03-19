##############################################
#  Main program for ESP32 with a single      #
#  DHT11 sensor                              #
#                                            #
#  KEA IT TEKNOLOG  -  IOT2 Projekt 2024     #
#  Gruppe 6C:                                #
#  Alexander Gundsø, Mads Janum Magnusson,   #
#  Emil Bøegh Grønning-Vogter &              #
#  Jacob Rusch Svendsen                      #
#                                            #
##############################################

from mqtt_as import MQTTClient, config
from utime import sleep
import asyncio
from machine import I2C, Pin
import json


####  Sensors  ####
import dht                             # DHT11
pin_dht11 = 32
sensor = dht.DHT11(Pin(pin_dht11))
# Battery
from adc_sub import ADC_substitute
pin_battery = 34                       # ADC1_6
battery = ADC_substitute(pin_battery)

# Activity LED
led = Pin(23, Pin.OUT)

# Local configuration
config['server'] = '52.236.38.161'  # Change to suit
config['ssid'] = 'iot'
config['wifi_pw'] = 'gruppe06'

def get_battery_percentage(battery):
    min_v = 1.59
    bat_v = battery.read_voltage()
    max_v = 2.27
    
    pct = int((bat_v - min_v)/(max_v-min_v)*100)
    if pct > 100:
        pct = 100
    if pct <= 0:
        pct = 0
    return(pct)

def reboot_esp():
    print("Rebooting!\n\n")
    import machine
    machine.reset()

async def messages(client):  # Respond to incoming messages
    async for topic, msg, retained in client.queue:
        print((topic, msg, retained))

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await client.subscribe('foo_topic', 1)  # renew subscriptions

async def main(client):
    try:
        await client.connect()
    except:
        print('Error')
        reboot_esp()
    
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))

    while True:
        await asyncio.sleep(30)
        led.on()
        
        #print('Publish', scd40_data)
        bat_pct = get_battery_percentage(battery)
        
        # Check the sensor
        sensor.measure()
        sensor_value_temp = sensor.temperature()
        sensor_value_hum = sensor.humidity()
        message = {
            "temp": sensor_value_temp,
            "hum":	sensor_value_hum,
            "bat": bat_pct
        }
        json_message = json.dumps(message)
        print("Publish:  ", json_message)

        await client.publish('sensor/bedroom/json', str(json_message), qos = 1)
        led.off()



config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors

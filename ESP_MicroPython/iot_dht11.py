from mqtt_as import MQTTClient, config
from utime import sleep
import asyncio
from machine import I2C, Pin

####  Sensors  ####
import dht                             # DHT11
pin_dht11 = 32
sensor = dht.DHT11(Pin(pin_dht11))
# Battery
pin_battery = 34                       # ADC1_6
batttery = ADC_substitute(pin_battery)

# Activity LED
led = Pin(23, Pin.OUT)

###  Calibrate  ###

#ens160.set_ambient_temp(float(scd40_data["temp"]))
#ens160.set_humidity(float(scd40_data["rh"]))

# Local configuration
config['server'] = '52.236.38.161'  # Change to suit
config['ssid'] = 'iot'
config['wifi_pw'] = 'gruppe06'

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
        await asyncio.sleep(10)
        led.on()

        #print('Publish', scd40_data)
        bat_pct = get_battery_percentage()

        # Check the sensor
        sensor.measure()
        sensor_value_temp = sensor.temperature()
        sensor_value_hum = sensor.humidity()

        await client.publish('sensor/dht11/temp', str(sensor_value_temp), qos = 1)
        led.off()



config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors



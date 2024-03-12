from mqtt_as import MQTTClient, config
from utime import sleep
import asyncio
from machine import I2C, Pin, time_pulse_us

####  Sensors  ####
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)
import ens160
ens160_tvoc = ens160.init(i2c)
import iot_scd40
scd40 = iot_scd40.init(i2c)
pm1006 = Pin(15, Pin.IN)

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
        scd40_data = iot_scd40.read(scd40)
        ens160_data = ens160.get_tvoc(ens160_tvoc)
        pm25_data = time_pulse_us(pm1006,0, 1_004_000) # Mål pulse længde(slukket), 1004 ms timeout
        print('Publish', scd40_data)
        print('Publish', ens160_data)
        # Udregn pulslængde til mikrogram per kubikmeter
        pm25_ug = int((((pm25_data - 4_000) * (992)) / (996_000 - 4_000)) + 0)
        print('Publish', pm25_ug)
        print(pm25_ug, " µg/m³")

        # If WiFi is down the following will pause for the duration.
        # Lidt spild at sende individuelt, så vi skal beslutte os om at sende én gang
        await client.publish('sensor/scd40/all', str(scd40_data), qos = 1)
       # await client.publish('sensor/scd40/co2', str(scd40_data["co2"]), qos = 1)
       # await client.publish('sensor/scd40/temp', str(scd40_data["temp"]), qos = 1)
       # await client.publish('sensor/scd40/rh', str(scd40_data["rh"]), qos = 1)
        await client.publish('sensor/ens160/tvoc', str(ens160_data), qos = 1)
        await client.publish('sensor/p1006/pm25', str(pm25_ug), qos = 1)
        led.off()



config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
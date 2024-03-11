from mqtt_as import MQTTClient, config
import asyncio

####  Sensors  ####
import iot_scd40
scd40 = iot_scd40.init()

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
        sensor_data = iot_scd40.read(scd40)
        print('Publish', sensor_data)
        # If WiFi is down the following will pause for the duration.
        # Lidt spild at sende individuelt, så vi skal beslutte os om at sende én gang
        await client.publish('sensor/scd40/all', str(sensor_data), qos = 1)
        await client.publish('sensor/scd40/co2', str(sensor_data["co2"]), qos = 1)
        await client.publish('sensor/scd40/temp', str(sensor_data["temp"]), qos = 1)
        await client.publish('sensor/scd40/rh', str(sensor_data["rh"]), qos = 1)


config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
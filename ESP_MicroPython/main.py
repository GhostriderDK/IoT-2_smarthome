import time
from mqtt_as import MQTTClient
from mqtt_local import wifi_led, blue_led, config
import uasyncio as asyncio

## SCD40 LIBS/SETUP ######################################
from scd4x_sensirion import SCD4xSensirion
from machine import I2C, Pin
from sensor_pack.bus_service import I2cAdapter

i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)
adaptor = I2cAdapter(i2c)
scd40 = SCD4xSensirion(adaptor)
scd40_masl = 68  # Metres Above Sea Level
scd40.set_altitude(scd40_masl)
scd40.set_measurement(start=False, single_shot=False)
##########################################################

# MQTT topic
TOPIC = 'sensor/test' 

outages = 0
sensor_value = "0"

def reboot_esp():
    print("Rebooting!\n\n")
    import machine
    machine.reset()

# async def pulse():  # This demo pulses blue LED each time a subscribed msg arrives.
#     blue_led(True)
#     await asyncio.sleep(1)
#     blue_led(False)

async def scd40_worker(scd40):
    sen.set_measurement(start=False, single_shot=False)
    sid = sen.get_id()
    print(f"Sensor id 3 x Word: {sid[0]:x}:{sid[1]:x}:{sid[2]:x}")
    # t_offs = 0.0
    # Warning: To change or read sensor settings, the SCD4x must be in idle mode!!!
    # Otherwise an EIO exception will be raised!
    # print(f"Set temperature offset sensor to {t_offs} Celsius")
    # sen.set_temperature_offset(t_offs)
    t_offs = sen.get_temperature_offset()
    print(f"Get temperature offset from sensor: {t_offs} Celsius")
    masl = 68  # Meter Above Sea Level
    print(f"Set my place M.A.S.L. to {masl} meter")
    sen.set_altitude(masl)
    masl = sen.get_altitude()
    print(f"Get M.A.S.L. from sensor: {masl} meter")
    # data ready
    if sen.is_data_ready():
        print("Measurement data can be read!")  # Данные измерений могут быть прочитаны!
    else:
        print("Measurement data missing!")
    
    if sen.is_auto_calibration():
        print("The automatic self-calibration is ON!")
    else:
        print("The automatic self-calibration is OFF!")

    sen.set_measurement(start=True, single_shot=False)      # periodic start
    wt = sen.get_conversion_cycle_time()
    print(f"conversion cycle time [ms]: {wt}")
    print("Periodic measurement started")
    repeat = 5
    multiplier = 2
    for i in range(repeat):
        time.sleep_ms(wt)
        co2, t, rh = sen.get_meas_data()
        print(f"CO2 [ppm]: {co2}; T [°C]: {t}; RH [%]: {rh}")
        sensor_value = f"CO2 [ppm]: {co2}; T [°C]: {t}; RH [%]: {rh}"

async def poll_sensor(client):
    global sensor_value
    scd40.set_measurement(start=True, single_shot=False)
    while True:
        if scd40.is_data_ready():
            print("Polling sensor")
            scd40.set_measurement(start=False, single_shot=True, rht_only=False)
            co2, t, rh = scd40.get_meas_data()
            print(f"CO2 [ppm]: {co2}; T [°C]: {t}; RH [%]: {rh}")
            sensor_value = f"CO2 [ppm]: {co2}; T [°C]: {t}; RH [%]: {rh}"
        await asyncio.sleep(10)

async def messages(client):
    async for topic, msg, retained in client.queue:
        print(f'Topic: "{topic.decode()}" Message: "{msg.decode()}" Retained: {retained}')
        asyncio.create_task(pulse())

async def down(client):
    global outages
    while True:
        await client.down.wait()  # Pause until connectivity changes
        client.down.clear()
        wifi_led(False)
        outages += 1
        print('WiFi or broker is down.')
        reboot_esp()

async def up(client):
    while True:
        await client.up.wait()
        client.up.clear()
        wifi_led(True)
        print('We are connected to broker.')
        await client.subscribe('foo_topic', 1)

async def main(client):
    try:
        await client.connect()
    except OSError:
        print('Connection failed.')
        reboot_esp()
        return
    for task in (up, down, poll_sensor):
        asyncio.create_task(task(client))
    n = 0
    while True:
        global sensor_value
        await asyncio.sleep(5)
        print('publish', sensor_value)
        # If WiFi is down the following will pause for the duration.
        await client.publish(TOPIC, sensor_value, qos = 1)
                

# Define configuration
config['will'] = (TOPIC, 'Goodbye cruel world!', False, 0)
config['keepalive'] = 120
config["queue_len"] = 1  # Use event interface with default queue

# Set up client. Enable optional debug statements.
MQTTClient.DEBUG = True
client = MQTTClient(config)

try:
    asyncio.run(main(client))
finally:  # Prevent LmacRxBlk:1 errors.
    client.close()
    blue_led(True)
    asyncio.new_event_loop()



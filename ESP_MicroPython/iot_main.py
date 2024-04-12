from mqtt_as import MQTTClient, config              # MQTT asynchronous library
from utime import sleep
import asyncio                                      # asyncio / asynchronous io, MQTT biblioteket bruger dette. Læs: https://docs.python.org/3/library/asyncio.html
from machine import I2C, Pin, PWM, time_pulse_us    # time_pulse_us fra machine modulet, tager tiden af en puls i mikrosekunder
import json

####  Sensors  ####
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000) # i2c objekt oprettet med en frekvens på 400 kHz (fast mode)
import ens160                                       
ens160_tvoc = ens160.init(i2c)                      # Opretter ens160 objekt og intitialiserer. ens160 lever på i2c bussen, hvorfor den skal have i2c objektet som parameter.
import iot_scd40
scd40 = iot_scd40.init(i2c)                         # Opretter scd40 object og initialiserer. SCD40 lever på i2c bussen, hvorfor den skal have i2c objektet som parameter
pm1006 = Pin(15, Pin.IN)                            # pm1006 partikelsensoren bliver til et "Pin" objekt

# Activity LED
led = Pin(23, Pin.OUT)

# Fan control
frequency = 25_000 # 25 KHz PWM frekvens
fan = PWM(14, frequency, duty=0)                    # duty=0, så blæseren starter slukket
# fan.duty(0)		= 0 %	duty cycle
# fan.duty(1023)	= 100 %	duty cycle

###  Calibrate  ###
#ens160.set_ambient_temp(float(scd40_data["temp"]))
#ens160.set_humidity(float(scd40_data["rh"]))

# Local configuration
config['server'] = 'iot2.northeurope.cloudapp.azure.com'  # Hostname på MQTT broker, dette er vores Azure VM
config['ssid'] = 'iot'
config['wifi_pw'] = 'gruppe06'

def reboot_esp():           # Bliver brugt hvis ESP ikke får forbindelse til WiFi eller MQTT broker
    print("Rebooting!\n\n")
    import machine
    machine.reset()

async def messages(client):  # Respond to incoming messages
    async for topic, msg, retained in client.queue:     # async udgaven af et for-loop, dvs. andre ting kan ske mens for-loopet bliver behandlet.
        print((topic, msg, retained))
        try:
            value = int(msg)
        except:
            print("Error converting message to integer")
        if value > 0:
            fan.duty(1023)
        elif value < 1:
            fan.duty(0)

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event, næste linje bliver først kørt når "up event" er sket
        client.up.clear()       # Clear the event. Ingen andre tasks venter på "up"-funktionen.
        await client.subscribe('sensor/stue/fan', 1)  # renew subscriptions

async def main(client): #### Primært loop hvor alt det vigtige sker. Først forbindes der til wifi og MQTT, derefter startes coroutines. Til sidst startes main while-loop. ####
    try:                                        # Prøver at forbinde til wifi og MQTT broker,
        await client.connect()                  # med "connect()" fra mqtt_as.
    except:                                     # Hvis dette ikke lykkes, genstarter vi hele ESPen.
        print('Error')
        reboot_esp()
    
    for coroutine in (up, messages):                # Starter bare funktionerne "up" og "messages" med et for-loop.
        asyncio.create_task(coroutine(client))      # Metoderne bliver startet som async tasks. Asynkrone opgaver

    while True:                                         # Primære while-loop
        await asyncio.sleep(10)                         # async udgave af "sleep()", blokerer ikke CPU'en
        led.on()                                        # Tænd LED mens vi sampler sensorer
        scd40_data = iot_scd40.read(scd40)              # Læser data fra scd40.     Se iot_scd40.py
        ens160_data = ens160.get_tvoc(ens160_tvoc)      # Læser data fra ens160.    Se ens160.py
        pm25_data = time_pulse_us(pm1006,0, 1_004_000)  # Mål puls-længde(slukket), 1004 ms timeout
        print('SCD40', scd40_data)
        print('ENS160', ens160_data)
        # Udregn pulslængde til mikrogram per kubikmeter
        pm25_ug = int((((pm25_data - 4_000) * (992)) / (996_000 - 4_000)) + 0)
        print(pm25_ug, " µg/m³")
        
        # Put values into a dictionary
        message = {
            "pm": pm25_ug,
            "tvoc": ens160_data
            }
        message.update(scd40_data) # Add dict from scd to dict.
        message_json = json.dumps(message)  # json.dumps() laver dict. til json-kompatibelt format
        print("Publish  ", message_json)

        # If WiFi is down the following will pause for the duration.        
        await client.publish('sensor/stue/json', str(message_json), qos = 1)    # Her bliver selve mqtt beskeden published (Topic, Message, QualityOfService)
        led.off()       # Sluk LED når vi har læst og afsendt sensordata. LED er tændt så længe MQTT beskeden ikke er blevet afsendt



config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)         # Her bliver selve MQTT klienten oprettet vha. mqtt_as biblioteket.
try:
    asyncio.run(main(client))   # kør main() som en async task. Læs: https://docs.python.org/3/library/asyncio.html
finally:
    client.close()  # Prevent LmacRxBlk:1 errors # ESP kommer aldrig til denne linje, da vi aldrig stopper main().
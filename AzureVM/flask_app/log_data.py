import sqlite3
from datetime import datetime
import json
import paho.mqtt.client as mqtt

print("subscribe mqtt script running")

topics = ["sensor/bedroom/json", "sensor/bad/json", "sensor/stue/json"]

def bath_message(client, userdata, message):
    query = """INSERT INTO bad (datetime, temperature, humidity, battery) VALUES(?, ?, ?, ?)"""
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")
    dht11_data = json.loads(message.payload.decode())
    data = (now, dht11_data['temp'], dht11_data['hum'], dht11_data['bat'])
    

    try:
        conn = sqlite3.connect("database/data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
                    
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Another error occured: {e}")
    finally:
        conn.close


def bedroom_message(client, userdata, message):
    query = """INSERT INTO bedroom (datetime, temperature, humidity, battery) VALUES(?, ?, ?, ?)"""
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")
    dht11_data = json.loads(message.payload.decode())
    data = (now, dht11_data['temp'], dht11_data['hum'], dht11_data['bat'])
    

    try:
        conn = sqlite3.connect("database/data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
                    
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Another error occured: {e}")
    finally:
        conn.close

def stue_message(client, userdata, message):
    query = """INSERT INTO stue (datetime, temperature, humidity, tvoc, particles, co2 ) VALUES(?, ?, ?, ?, ?, ?)"""
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")
    stue_data = json.loads(message.payload.decode())
    data = (now, stue_data['temp'], stue_data['rh'], stue_data['tvoc'], stue_data['pm'], stue_data['co2'])
    

    try:
        conn = sqlite3.connect("database/data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
                    
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Another error occured: {e}")
    finally:
        conn.close



def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to topics upon connection
    client.subscribe("sensor/bad/json")
    client.subscribe("sensor/bedroom/json")
    client.subscribe("sensor/stue/json")

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")
    # Call appropriate callback function based on topic
    if message.topic == "sensor/bad/json":
        bath_message(client, userdata, message)
    elif message.topic == "sensor/bedroom/json":
        bedroom_message(client, userdata, message)
    elif message.topic == "sensor/stue/json":
        stue_message(client, userdata, message)

client = mqtt.Client()

# Assign on_connect and on_message callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to local MQTT broker
client.connect("127.0.0.1", 1883)

# Start the MQTT client loop
client.loop_forever()
#subscribe.callback(bath_message, "sensor/bad/json", hostname="localhost", userdata={"message_count": 0})
#subscribe.callback(bedroom_message, "sensor/bedroom/json", hostname="localhost", userdata={"message_count": 0})
#subscribe.callback(stue_message, "sensor/stue/json", hostname="localhost", userdata={"message_count": 0})

#while True:
#    pass
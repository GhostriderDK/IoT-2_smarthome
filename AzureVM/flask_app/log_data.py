import sqlite3
from datetime import datetime
import json
import paho.mqtt.subscribe as subscribe

print("subscribe mqtt script running")


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

topic_function_map = {
    "sensor/bad/json": bath_message,
    "sensor/bedroom/json": bedroom_message,
    "sensor/stue/json": stue_message
}


def on_message_received(client, userdata, message):
    topic = message.topic
    if topic in topic_function_map:
        topic_function_map[topic](client, userdata, message)
    else:
        print(f"No function mapped for topic: {topic}")

topics = ["sensor/bedroom/json", "sensor/bad/json", "sensor/stue/json"]
subscribe.callback(on_message_received, topics, hostname="localhost", userdata={"message_count": 0})
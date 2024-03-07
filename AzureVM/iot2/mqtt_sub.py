import paho.mqtt.subscribe as subscribe

print("Subscribe MQTT running")

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    userdata["message_count"] += 1
    if userdata["message_count"] >= 5:
        client.disconnect()

#subscribe.callback(on_message_print, "paho/test/topic", hostname="iot2.northeurope.cloudapp.azure.com", userdata={"message_count": 0})
subscribe.callback(on_message_print, "paho/test/topic", hostname="localhost", userdata={"message_count": 0})
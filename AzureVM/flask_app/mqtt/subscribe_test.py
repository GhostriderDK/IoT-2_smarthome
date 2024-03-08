import paho.mqtt.subscribe as subscribe

print("subscribe mqtt script running")

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

subscribe.callback(on_message_print, "paho/test/topic", hostname="localhost", userdata={"message_count": 0})
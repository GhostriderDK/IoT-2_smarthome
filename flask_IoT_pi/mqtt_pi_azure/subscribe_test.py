import paho.mqtt.subscribe as subscribe
from gpiozero import LED

red = LED(17)

print("subscribe mqtt script running")

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    status = message.payload.decode()

    if status == 'teand':
        red.on()
    if status == 'sluk':
        red.off()

subscribe.callback(on_message_print, "LED", hostname="74.234.16.65", userdata={"message_count": 0})
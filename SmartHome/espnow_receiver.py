# https://docs.micropython.org/en/latest/library/espnow.html
import network
import espnow

# A WLAN interface must be active to send()/recv()
station = network.WLAN(network.STA_IF)
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)

while True:
    host, msg = esp_now.recv()
    if msg:             # msg == None if timeout in recv()
        print(host, msg)
        if msg == b'end':
            break
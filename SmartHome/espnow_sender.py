# https://docs.micropython.org/en/latest/library/espnow.html
import network
import espnow

# A WLAN interface must be active to send()/recv()
station = network.WLAN(network.STA_IF)  # Or network.AP_IF
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)
peer = b'\xff\xff\xff\xff\xff\xff'   # MAC address of peer's wifi interface
esp_now.add_peer(peer)      # Must add_peer() before send()

esp_now.send(peer, "Starting...")
for i in range(100):
    esp_now.send(peer, str(i)*20, True)
esp_now.send(peer, b'end')
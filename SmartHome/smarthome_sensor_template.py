# Smart Home sensor program
# MicroPython and ESP32 https://docs.micropython.org/en/latest/esp32/quickref.html
# https://docs.micropython.org/en/latest/library/espnow.html

import network
import espnow

from machine import ADC, Pin
import time

########################################
# OWN MODULES
from adc_sub import ADC_substitute

########################################
# CONFIGURATION
dashboard_mac_address = b'\xA1\xB2\xC3\xD4\xE5\xF6' # MAC address of dashboard (Educaboard). Byte string format!

########################################
# OBJECTS
# ESP-NOW
sta = network.WLAN(network.STA_IF)     # Or network.AP_IF
sta.active(True)                       # WLAN interface must be active to send()/recv()

en = espnow.ESPNow()                   # ESP-NOW object
en.active(True)                        # Make ESP-NOW active

# Sensor
pin_sensor_input_analog = 1            # The sensor analog GPIO input pin
pin_sensor_input_digital = 33          # The sensor digital GPIO input pin
sensor_d = Pin(pin_sensor_input_digital, Pin.IN)
pin_sensor_output = 3                  # The sensor output GPIO pin

# Battery
pin_battery = 34                       # The battery measurement input pin, ADC1_6
adc_bat = ADC_substitute(pin_battery)  # The battery ADC object

########################################
# VARIABLES
sensor_id = "The sensor ID"            # The sensor ID

# Previous values
prev_sensor_value = -999               # The previous value from the sensor
prev_bat_pct = -1                      # The previous battery percentage value

########################################
# FUNCTIONS
def get_battery_percentage():          # The battery voltage percentage
    return 24                          # Replace with own math. Use function in adc_sub.py
                                       # Make the result an integer value, and avoid neg. and above 100% values
                                       
########################################
# PROGRAM

# INITIALIZATION
# ESP-NOW
en.add_peer(dashboard_mac_address)     # Must add_peer() before send()
en.send(dashboard_mac_address, sensor_id + " ready", False)

print(sensor_id + " ready")

# MAIN (super loop)
while True:
    # Measure the battery percentage
    bat_pct = get_battery_percentage()
    
    # Check the sensor
    sensor_value = 0

    # Send data if there is a change (this principle saves power)
    if bat_pct != prev_bat_pct or sensor_value != prev_sensor_value:
        data_string = str(time.ticks_ms()) + '|' + str(bat_pct) + '|' + str(sensor_value) # The data to send. CHANGE IT!
        
        print("Sending: " + data_string)
        try:
            en.send(dashboard_mac_address, data_string, False)
        except ValueError as e:
            print("Error sending the message: " + str(e))  
        
        # Update the previous values for use next time
        prev_bat_pct = bat_pct
        prev_sensor_value = sensor_value

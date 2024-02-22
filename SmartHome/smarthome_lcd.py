# Smart Home LCD handling functions module

#######################################
# IMPORTS
from machine import Pin
from time import sleep
import network

from gpio_lcd import GpioLcd           # LCD

#######################################
# OBJECTS
lcd = GpioLcd(rs_pin = Pin(27), enable_pin = Pin(25),   # Create the LCD object
              d4_pin = Pin(33), d5_pin = Pin(32), d6_pin = Pin(21), d7_pin = Pin(22),
              num_lines = 4, num_columns = 20)

#######################################
# FUNCTIONS

# Prints a splash screen on the display and USB port
def print_splash_screen(strings):
    for i in range(4):
        lcd.putstr(strings[i])         # Print on the display
        
# Preformat the LCD layout for real use, once the splash screen is done
def preformat_screen():
    
    return # remove when the layout design is done

#     lcd.clear()
#     lcd.move_to(0, 1)
#     lcd.putstr("La:")
#     lcd.move_to(0, 2)
#     lcd.putstr("Lo:")
#     lcd.move_to(14, 2)
#     lcd.putstr("A:")
#     lcd.move_to(0, 3)
#     

def print_broadcast(msg):
    lcd.move_to(0, 3)
    lcd.putstr(msg)
    
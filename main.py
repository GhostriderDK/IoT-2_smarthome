import RPi.GPIO as GPIO
import dht11
import time

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Define pins for DHT11 sensor, pump control, and LED control
DHT_PIN = 7     # GPIO 4 (Pin 7) for DHT11 data
PUMP_PIN = 18   # GPIO 18 (Pin 12) for pump control
RED_LED_PIN = 12  # GPIO 12 (Pin 32) for red LEDs
BLUE_LED_PIN = 13  # GPIO 13 (Pin 33) for blue LEDs (Example pin)

# Set up PWM for LED control
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)
red_pwm = GPIO.PWM(RED_LED_PIN, 1000)  # Frequency 1 kHz
blue_pwm = GPIO.PWM(BLUE_LED_PIN, 1000)

# Set up pump control
GPIO.setup(PUMP_PIN, GPIO.OUT)
GPIO.output(PUMP_PIN, GPIO.LOW)  # Make sure pump is initially off

# Initialize DHT11 sensor
instance = dht11.DHT11(pin=DHT_PIN)

def read_dht11():
    result = instance.read()
    if result.is_valid():
        temperature = result.temperature
        humidity = result.humidity
        print("Temperature: {}°C, Humidity: {}%".format(temperature, humidity))
    else:
        print("Failed to read data from DHT11")

def control_pump(on):
    if on:
        GPIO.output(PUMP_PIN, GPIO.HIGH)  # Turn pump on
        print("Pump is ON")
    else:
        GPIO.output(PUMP_PIN, GPIO.LOW)  # Turn pump off
        print("Pump is OFF")

def control_leds(red_intensity, blue_intensity):
    red_pwm.start(red_intensity)   # Start PWM with specified intensity (0-100)
    blue_pwm.start(blue_intensity)

# Main function to control pump, LEDs, and read DHT11
def main():
    try:
        while True:
            # Read DHT11 sensor data
            read_dht11()
            
            # Example: Turn pump on for 5 seconds, then off for 5 seconds
            control_pump(True)
            control_leds(50, 75)  # Example intensity values (0-100)
            time.sleep(5)
            control_pump(False)
            control_leds(0, 0)  # Turn off LEDs
            time.sleep(5)

    except KeyboardInterrupt:
        # Clean up GPIO
        GPIO.cleanup()

if __name__ == "__main__":
    main()
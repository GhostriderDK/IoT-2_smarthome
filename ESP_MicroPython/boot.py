# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import time
print("Sleeping 3 seconds before starting application. Press Ctrl+C to stop.")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
print("0")
while True:
    import main
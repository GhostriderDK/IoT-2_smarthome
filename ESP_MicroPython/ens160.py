from machine import I2C, Pin
import ens160sciosense
from sensor_pack.bus_service import I2cAdapter
import time

def init(i2c):
    #i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000) 
    adaptor = I2cAdapter(i2c)
    
    gas_sens = ens160sciosense.Ens160(adaptor)

    gas_sens.set_mode(0x02)
    gs_id = gas_sens.get_id()
    print(f"Sensor ID: {hex(gs_id)}")
        
    fw = gas_sens.get_firmware_version()
    print(f"Firmware version: {fw}")
    st = gas_sens.get_status()
    print(f"Status: {hex(st)}")
    return gas_sens

def read(gas_sens):
    for eco2, tvoc, aqi in gas_sens:
        print(f"CO2: {eco2}\tTVOC: {tvoc}\tAQI: {aqi}")
        return str(tvoc)
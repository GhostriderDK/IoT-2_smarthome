# An ESP32 ADC substituting library usable from 200 mV to 2,4 V
#
# This library mitigates some of the ESP32 ADC problems:
# - noise: by averaging over 256 measurement
# - 100 mV late start, and 
# - non linearity: by using own formula
#
# The library uses a fixed attenuation of 11 dB and 12 bits

from machine import ADC, Pin

class ADC_substitute():

    __adc = None
    
    # ADC value to voltage first degree equation coefficients
    __alpha = 0.000838616
    __beta = 0.097068
    
    
    def __init__(self, pin_adc):
        self.__adc = ADC(Pin(pin_adc))
        self.__adc.atten(ADC.ATTN_11DB)
        self.__adc.width(ADC.WIDTH_12BIT) 
        
        
    def read_adc(self):
        adc_val = 0
        for i in range(256):
            adc_val += self.__adc.read()
        adc_val = adc_val >> 8
        
        return adc_val
    
    
    def read_voltage(self):
        adc_val = self.read_adc()
       
        return self.__alpha * adc_val + self.__beta

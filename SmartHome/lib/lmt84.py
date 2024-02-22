# A library to use one of the LMT84 temperature sensors using
# an ESP32. Normally using an analog sensor is straight
# forward with an MCU. But the ADCs in the ESP32 is the worst
# implementation of an ADCs ever seen.
# IT IS SILICON ABUSE.
#
# ESP32-ADC is not: U = Umax * ADC / (2^bit_width - 1)
# thus ADC is not : ADC = U * (2^bit_width - 1) / Umax
#
# This library mitigates some of the problems:
# - noise: by averaging over a series of measurement
# - 100 mV late start, and 
# - non linearity: by enabling in situ calibration
#
# How to calibrate
#   You only need to do this ones, if you save alpha and beta
#   Make a note of the Temperature1 and the return ADC1 value from get_adc_value()
#   Change the temperature and let the temperature around the LMT84 settle
#   Make a note of the Temperature2 and the return ADC2 value from get_adc_value()
#   In the main program save the Temperature1, ADC1, Temperature2, ADC2 values
#   Evoke calibrate(Temperature1, ADC1, Temperature2, ADC2)


from machine import ADC, Pin

class LMT84:
    __alpha = -0.06268221
    __beta = 188.0466472
    __adc = None


    def __init__(self, pin_adc, alpha = -0.062682216, beta = 188.0466472):
        
        self.__adc = ADC(Pin(pin_adc))
        # 100 mV to 1,25 V, i.e. from about -40 °C and up to 150 °C
        # Modify this for the LMT85, LMT86 or LMT87 all having a wider voltage range
        self.__adc.atten(ADC.ATTN_2_5DB)
        # The width affects the calibration, i.e. adc1 and adc2 thus alpha, beta
        # Set here just in case it was set to another width outside this library
        self.__adc.width(ADC.WIDTH_12BIT) 

        self.__alfa = alpha
        self.__beta = beta
    
    
    # Calculate the alpha and beta values in the temp = alpha adc + beta equation
    # If adc1 = adc2 then calibration is not done and the function returns None, otherise alpha and beta values are returned
    def calibrate(self, temp1, adc1, temp2, adc2):
        
        if adc1 == adc2:               # Invalid values when adc1 = adc2 as it leads to a divide by zero
            return None
            
        self.__alpha = (temp2 - temp1) / (adc2 - adc1)
        self.__beta = temp2 - self.__alpha * adc2   # or beta = temp1 - alpha * adc1
        
        return self.__alpha, self.__beta


    # Returns the value from the ADC averaged over 256 measurements
    def get_adc_value(self):
        self.__adc.width(ADC.WIDTH_12BIT) # "Reset" here just in case it was changed to another width outside this library
        
        adc_val = 0
        for i in range(256):
            adc_val += self.__adc.read()
        adc_val = adc_val >> 8
        
        return adc_val
    

    # Returns the temperature averaged over avg_exp measurements
    def get_temperature(self, avg_exp = 6):
        
        if avg_exp in (0, 1, 2, 4, 5, 6, 7, 8): # 2^0 = 1, 2^1 = 2, 2^2 = 4, ... 2^8 = 256
            
            self.__adc.width(ADC.WIDTH_12BIT) # "Reset" here just in case it was set to another width outside this library
        
            adc_val = 0
            for i in range(1 << avg_exp): 
                adc_val += self.__adc.read()
            adc_val = adc_val >> avg_exp
            
            temp = self.__alpha * adc_val + self.__beta

            return temp

        # Invalid average exponent
        return None

# Library to use with an INA219 current monitor device
#
# Initialize parameters
#    I2C bus
#    I2C address
#
#    Default settings are:
#        32 V
#         2 A
#        100 mohms shunt resistor
#        12 bits ADCs

# Bits
_READ = const(0x01)

# Config Register (R/W)
_REG_CONFIG = const(0x00)
_CONFIG_RESET = const(0x8000)                     # Reset Bit

_CONFIG_BVOLTAGERANGE_MASK = const(0x2000)        # Bus Voltage Range Mask
_CONFIG_BVOLTAGERANGE_16V = const(0x0000)         # 0-16 V Range
_CONFIG_BVOLTAGERANGE_32V = const(0x2000)         # 0-32 V Range

_CONFIG_GAIN_MASK = const(0x1800)                 # Gain Mask
_CONFIG_GAIN_1_40MV = const(0x0000)               # Gain 1, 40 mV Range
_CONFIG_GAIN_2_80MV = const(0x0800)               # Gain 2, 80 mV Range
_CONFIG_GAIN_4_160MV = const(0x1000)              # Gain 4, 160 mV Range
_CONFIG_GAIN_8_320MV = const(0x1800)              # Gain 8, 320 mV Range

_CONFIG_BADCRES_MASK = const(0x0780)              # Bus ADC Resolution Mask
_CONFIG_BADCRES_9BIT = const(0x0080)              #  9 bit bus res = 0..511
_CONFIG_BADCRES_10BIT = const(0x0100)             # 10 bit bus res = 0..1023
_CONFIG_BADCRES_11BIT = const(0x0200)             # 11 bit bus res = 0..2047
_CONFIG_BADCRES_12BIT = const(0x0400)             # 12 bit bus res = 0..4095

_CONFIG_SADCRES_MASK = const(0x0078)              # Shunt ADC resistor and avg mask
_CONFIG_SADCRES_9BIT_1S_84US = const(0x0000)      # 1 x 9 bit shunt sample
_CONFIG_SADCRES_10BIT_1S_148US = const(0x0008)    # 1 x 10 bit shunt sample
_CONFIG_SADCRES_11BIT_1S_276US = const(0x0010)    # 1 x 11 bit shunt sample
_CONFIG_SADCRES_12BIT_1S_532US = const(0x0018)    # 1 x 12 bit shunt sample
_CONFIG_SADCRES_12BIT_2S_1060US = const(0x0048)   # 2 x 12 bit sample average
_CONFIG_SADCRES_12BIT_4S_2130US = const(0x0050)   # 4 x 12 bit sample average
_CONFIG_SADCRES_12BIT_8S_4260US = const(0x0058)   # 8 x 12 bit sample average
_CONFIG_SADCRES_12BIT_16S_8510US = const(0x0060)  # 16 x 12 bit sample average
_CONFIG_SADCRES_12BIT_32S_17MS = const(0x0068)    # 32 x 12 bit sample average
_CONFIG_SADCRES_12BIT_64S_34MS = const(0x0070)    # 64 x 12 bit sample average
_CONFIG_SADCRES_12BIT_128S_69MS = const(0x0078)   # 128 x 12 bit sample average

# Operating Mode Mask
_CONFIG_MODE_MASK = const(0x0007)  
_CONFIG_MODE_POWERDOWN = const(0x0000)
_CONFIG_MODE_SVOLT_TRIGGERED = const(0x0001)
_CONFIG_MODE_BVOLT_TRIGGERED = const(0x0002)
_CONFIG_MODE_SANDBVOLT_TRIGGERED = const(0x0003)
_CONFIG_MODE_ADCOFF = const(0x0004)
_CONFIG_MODE_SVOLT_CONTINUOUS = const(0x0005)
_CONFIG_MODE_BVOLT_CONTINUOUS = const(0x0006)
_CONFIG_MODE_SANDBVOLT_CONTINUOUS = const(0x0007)

# SHUNT VOLTAGE REGISTER (R)
_REG_SHUNTVOLTAGE = const(0x01)

# BUS VOLTAGE REGISTER (R)
_REG_BUSVOLTAGE = const(0x02)

# POWER REGISTER (R)
_REG_POWER = const(0x03)

# CURRENT REGISTER (R)
_REG_CURRENT = const(0x04)

# CALIBRATION REGISTER (R/W)
_REG_CALIBRATION = const(0x05)


def _to_signed(num):
    if num > 0x7FFF:
        num -= 0x10000
    return num


class INA219:

    def __init__(self, i2c_device, addr = 0x40):
        self.i2c_device = i2c_device

        self.i2c_addr = addr
        self.buf = bytearray(2)
        # Multiplier in mA used to determine current from raw reading
        self._current_lsb = 0
        # Multiplier in W used to determine power from raw reading
        self._power_lsb = 0

        # Set the INA219 to max values for safety reasons
        self._cal_value = 4096
        self.set_calibration_32V_2A()

    
    def write_register(self, reg, value):
        self.buf[0] = (value >> 8) & 0xFF
        self.buf[1] = value & 0xFF
        self.i2c_device.writeto_mem(self.i2c_addr, reg, self.buf)

    
    def read_register(self, reg):
        self.i2c_device.readfrom_mem_into(self.i2c_addr, reg & 0xff, self.buf)
        value = (self.buf[0] << 8) | (self.buf[1])
        
        return value


    def get_shunt_voltage(self):       # The voltage over the shunt resistor
        value = _to_signed(self.read_register(_REG_SHUNTVOLTAGE))
        
        return value * 0.00001         # The least signficant bit is 10 uV


    def get_bus_voltage(self):         # The voltage on the load, i.e. V- and ground
        raw_voltage = self.read_register(_REG_BUSVOLTAGE)

        # Shift to the right 3 to drop CNVR and OVF and multiply by LSB
        # Each least signficant bit is 4 mV
        voltage_mv = _to_signed(raw_voltage >> 3) * 4

        return voltage_mv * 0.001


    def get_current(self):             # The current to the load in mA
        # Sometimes a sharp load will reset the INA219, which will
        # reset the cal register, meaning CURRENT and POWER will
        # not be available ... as this by always setting a cal
        # value even if it's an unfortunate extra step
        self.write_register(_REG_CALIBRATION, self._cal_value)
        # Now we can safely read the CURRENT register!
        raw_current = _to_signed(self.read_register(_REG_CURRENT))
        
        return raw_current * self._current_lsb

    
    def set_calibration_32V_2A(self):  # pylint: disable=invalid-name
        """Configures to INA219 to be able to measure up to 32 V and 2 A
            of current. Counter overflow occurs at 3.2 A
           ..note :: These calculations assume a 0.1 ohm resistor"""
        # By default we use a pretty huge range for the input voltage,
        # which probably isn't the most appropriate choice for system
        # that don't use a lot of power.  But all of the calculations
        # are shown below if you want to change the settings.  You will
        # also need to change any relevant register settings, such as
        # setting the VBUS_MAX to 16V instead of 32 V, etc.

        # VBUS_MAX = 32V    (Assumes 32 V, can also be set to 16 V)
        # VSHUNT_MAX = 0.32 (Assumes Gain 8, 320 mV, can also be
        #                    0.16, 0.08, 0.04)
        # RSHUNT = 0.1      (Resistor value in ohms)

        # 1. Determine max possible current
        # MaxPossible_I = VSHUNT_MAX / RSHUNT
        # MaxPossible_I = 3.2 A

        # 2. Determine max expected current
        # MaxExpected_I = 2.0 A

        # 3. Calculate possible range of LSBs (Min = 15 bit, Max = 12 bit)
        # MinimumLSB = MaxExpected_I/32767
        # MinimumLSB = 61 uA per bit
        # MaximumLSB = MaxExpected_I/4096
        # MaximumLSB = 488 uA per bit

        # 4. Choose an LSB between the min and max values
        #    (Preferrably a roundish number close to MinLSB)
        # CurrentLSB = 100 uA per bit
        self._current_lsb = .1         # Current LSB = 100 uA per bit

        # 5. Compute the calibration register
        # Cal = trunc (0.04096 / (Current_LSB * RSHUNT))
        # Cal = 4096 (0x1000)

        self._cal_value = 4096

        # 6. Calculate the power LSB
        # PowerLSB = 20 * CurrentLSB
        # PowerLSB = 2 mW per bit
        self._power_lsb = .002         # Power LSB = 2 mW per bit

        # 7. Compute the maximum current and shunt voltage values before
        #    overflow
        #
        # Max_Current = Current_LSB * 32767
        # Max_Current = 3.2767 A before overflow
        #
        # If Max_Current > Max_Possible_I then
        #    Max_Current_Before_Overflow = MaxPossible_I
        # Else
        #    Max_Current_Before_Overflow = Max_Current
        # End If
        #
        # Max_ShuntVoltage = Max_Current_Before_Overflow * RSHUNT
        # Max_ShuntVoltage = 0.32 V
        #
        # If Max_ShuntVoltage >= VSHUNT_MAX
        #    Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
        # Else
        #    Max_ShuntVoltage_Before_Overflow = Max_ShuntVoltage
        # End If

        # 8. Compute the Maximum Power
        # MaximumPower = Max_Current_Before_Overflow * VBUS_MAX
        # MaximumPower = 3.2 * 32 V
        # MaximumPower = 102.4 W

        # Set Calibration register to 'Cal' calculated above
        self.write_register(_REG_CALIBRATION, self._cal_value)

        # Set Config register to take into account the settings above
        config = (_CONFIG_BVOLTAGERANGE_32V |
                  _CONFIG_GAIN_8_320MV |
                  _CONFIG_BADCRES_12BIT |
                  _CONFIG_SADCRES_12BIT_1S_532US |
                  _CONFIG_MODE_SANDBVOLT_CONTINUOUS)
        self.write_register(_REG_CONFIG, config)

    
    def set_calibration_32V_1A(self):  # pylint: disable=invalid-name
        """Configures to INA219 to be able to measure up to 32 V and 1 A of
           current. Counter overflow occurs at 1.3 A
           .. note:: These calculations assume a 0.1 ohm shunt resistor."""
        # By default we use a pretty huge range for the input voltage,
        # which probably isn't the most appropriate choice for system
        # that don't use a lot of power.  But all of the calculations
        # are shown below if you want to change the settings.  You will
        # also need to change any relevant register settings, such as
        # setting the VBUS_MAX to 16 V instead of 32 V, etc.

        # VBUS_MAX = 32 V    (Assumes 32 V, can also be set to 16 V)
        # VSHUNT_MAX = 0.32 (Assumes Gain 8, 320 mV, can also be
        #                    0.16, 0.08, 0.04)
        # RSHUNT = 0.1      (Resistor value in ohms)

        # 1. Determine max possible current
        # MaxPossible_I = VSHUNT_MAX / RSHUNT
        # MaxPossible_I = 3.2 A

        # 2. Determine max expected current
        # MaxExpected_I = 1.0 A

        # 3. Calculate possible range of LSBs (Min = 15 bit, Max = 12 bit)
        # MinimumLSB = MaxExpected_I/32767
        # MinimumLSB = 30.5uA per bit
        # MaximumLSB = MaxExpected_I/4096
        # MaximumLSB = 244 uA per bit

        # 4. Choose an LSB between the min and max values
        #    (Preferrably a roundish number close to MinLSB)
        # CurrentLSB = 40 uA per bit
        self._current_lsb = 0.04  # In mA

        # 5. Compute the calibration register
        # Cal = trunc (0.04096 / (Current_LSB * RSHUNT))
        # Cal = 10240 (0x2800)

        self._cal_value = 10240

        # 6. Calculate the power LSB
        # PowerLSB = 20 * CurrentLSB
        # PowerLSB = 800 uW per bit
        self._power_lsb = 0.0008

        # 7. Compute the maximum current and shunt voltage values before
        #    overflow
        #
        # Max_Current = Current_LSB * 32767
        # Max_Current = 1.31068 A before overflow
        #
        # If Max_Current > Max_Possible_I then
        #    Max_Current_Before_Overflow = MaxPossible_I
        # Else
        #    Max_Current_Before_Overflow = Max_Current
        # End If
        #
        # ... In this case, we're good though since Max_Current is less than
        #     MaxPossible_I
        #
        # Max_ShuntVoltage = Max_Current_Before_Overflow * RSHUNT
        # Max_ShuntVoltage = 0.131068 V
        #
        # If Max_ShuntVoltage >= VSHUNT_MAX
        #    Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
        # Else
        #    Max_ShuntVoltage_Before_Overflow = Max_ShuntVoltage
        # End If

        # 8. Compute the Maximum Power
        # MaximumPower = Max_Current_Before_Overflow * VBUS_MAX
        # MaximumPower = 1.31068 * 32 V
        # MaximumPower = 41.94176 W

        # Set Calibration register to 'Cal' calculated above
        self.write_register(_REG_CALIBRATION, self._cal_value)

        # Set Config register to take into account the settings above
        config = (_CONFIG_BVOLTAGERANGE_32V |
                  _CONFIG_GAIN_8_320MV |
                  _CONFIG_BADCRES_12BIT |
                  _CONFIG_SADCRES_12BIT_1S_532US |
                  _CONFIG_MODE_SANDBVOLT_CONTINUOUS)
        self.write_register(_REG_CONFIG, config)

    
    def set_calibration_16V_400mA(self):  # pylint: disable=invalid-name
        """Configures to INA219 to be able to measure up to 16 V and 400 mA of
           current. Counter overflow occurs at 1.6 A
           .. note:: These calculations assume a 0.1 ohm shunt resistor."""
        # Calibration which uses the highest precision for
        # current measurement (0.1 mA), at the expense of
        # only supporting 16 V at 400 mA max.

        # VBUS_MAX = 16 V
        # VSHUNT_MAX = 0.04          (Assumes Gain 1, 40 mV)
        # RSHUNT = 0.1               (Resistor value in ohms)

        # 1. Determine max possible current
        # MaxPossible_I = VSHUNT_MAX / RSHUNT
        # MaxPossible_I = 0.4 A

        # 2. Determine max expected current
        # MaxExpected_I = 0.4 A

        # 3. Calculate possible range of LSBs (Min = 15 bit, Max = 12 bit)
        # MinimumLSB = MaxExpected_I/32767
        # MinimumLSB = 12uA per bit
        # MaximumLSB = MaxExpected_I/4096
        # MaximumLSB = 98uA per bit

        # 4. Choose an LSB between the min and max values
        #    (Preferrably a roundish number close to MinLSB)
        # CurrentLSB = 50 uA per bit
        self._current_lsb = 0.05  # in mA

        # 5. Compute the calibration register
        # Cal = trunc (0.04096 / (Current_LSB * RSHUNT))
        # Cal = 8192 (0x2000)

        self._cal_value = 8192

        # 6. Calculate the power LSB
        # PowerLSB = 20 * CurrentLSB
        # PowerLSB = 1 mW per bit
        self._power_lsb = 0.001

        # 7. Compute the maximum current and shunt voltage values before
        #    overflow
        #
        # Max_Current = Current_LSB * 32767
        # Max_Current = 1.63835A before overflow
        #
        # If Max_Current > Max_Possible_I then
        #    Max_Current_Before_Overflow = MaxPossible_I
        # Else
        #    Max_Current_Before_Overflow = Max_Current
        # End If
        #
        # Max_Current_Before_Overflow = MaxPossible_I
        # Max_Current_Before_Overflow = 0.4
        #
        # Max_ShuntVoltage = Max_Current_Before_Overflow * RSHUNT
        # Max_ShuntVoltage = 0.04 V
        #
        # If Max_ShuntVoltage >= VSHUNT_MAX
        #    Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
        # Else
        #    Max_ShuntVoltage_Before_Overflow = Max_ShuntVoltage
        # End If
        #
        # Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
        # Max_ShuntVoltage_Before_Overflow = 0.04 V

        # 8. Compute the Maximum Power
        # MaximumPower = Max_Current_Before_Overflow * VBUS_MAX
        # MaximumPower = 0.4 * 16 V
        # MaximumPower = 6.4 W

        # Set Calibration register to 'Cal' calculated above
        self.write_register(_REG_CALIBRATION, self._cal_value)

        # Set Config register to take into account the settings above
        config = (_CONFIG_BVOLTAGERANGE_16V |
                  _CONFIG_GAIN_1_40MV |
                  _CONFIG_BADCRES_12BIT |
                  _CONFIG_SADCRES_12BIT_1S_532US |
                  _CONFIG_MODE_SANDBVOLT_CONTINUOUS)
        self.write_register(_REG_CONFIG, config)

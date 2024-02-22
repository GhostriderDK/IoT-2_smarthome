# Library to use an MCP23S08 port expander via SPI
#
# Initialize parameters
#    SPI bus
#    Port expander CS pin number
#    Port expander address
#
# Available functions
#    read_register(register)
#    write_register(register)
#
#    gp_direction(gp, val)
#    gp_interrupt(gp, val)
#    gp_pullup(gp, val)
#
#    gp_get_value(gp)
#    gp_set_value(gp, val)

from machine import Pin

class PortExp_MCP23S08():
    # GENERIC CONSTANTS, ought to be program global enums
    ON      = const(1)
    OFF     = const(0)

    INPUT   = const(1)
    OUTPUT  = const(0)

    # MCP23S08 REGISTERS, ought to be global enums
    IODIR   = const(0x00)                   # I/O direction register
    IPOL    = const(0x01)                   # Input polarity port register
    GPINTEN = const(0x02)                   # Interrupt register
    DEFVAL  = const(0x03)                   # Default value register
    INTCON  = const(0x04)                   # Interrupt-on-change control register
    IOCON   = const(0X05)                   # I/O expander configuration register
    GPPU    = const(0x06)                   # Pull-up register
    INTF    = const(0x07)                   # Interrupt flag register
    INTCAP  = const(0x08)                   # Read-only
    GPIO    = const(0x09)                   # GPIO value register
    OLAT    = const(0x0A)                   # Output latch register    
    
    
    def __init__(self, spi_bus, pin_cs, addr = 0):
        self.spi_bus = spi_bus
        self.pin_cs = Pin(pin_cs, Pin.OUT)  # Create the SS/CS (L) pin
        self.addr = addr
        
       
    def read_register(self, register):
        self.pin_cs.value(0)                # Set CS low, i.e. enable the MCP23S08
        
        ba = bytearray(3)                   # Prepare the bytes to send, one more than sent because the read value is located in the last byte
        ba[0] = 0x41 | (self.addr << 1)
        ba[1] = register
        self.spi_bus.write_readinto(ba, ba)
        val = ba[2]                         # Read the byte that is locate in the array + 1 thus [2]!
        
        self.pin_cs.value(1)                # Set CS high, i.e. disable the MCP23S08
        
        return val
        
        
    def write_register(self, register, val):
        self.pin_cs.value(0)                # Set CS low, i.e. enable the MCP23S08
        
        ba = bytearray(3)                   # Prepare the bytes to send
        ba[0] = 0x40 | (self.addr << 1)
        ba[1] = register
        ba[2] = val
        self.spi_bus.write(ba)
        
        self.pin_cs.value(1)                # Set CS high, i.e. disable the MCP23S08
       
       
    def gp_direction(self, gp, val):
        if gp < 0 or gp > 7 or (val != OUTPUT and val != INPUT): # Check the input parameters
            return
        
        reg_val = self.read_register(IODIR) # Read the current status of the register
        if val == OUTPUT:                   # Direction is output
            reg_val &= ~(1 << gp)
        else:                               # Direction is input
            reg_val |= 1 << gp
        self.write_register(IODIR, reg_val) # Write the updated value of the register
        
        
    def gp_interrupt(self, gp, val):
        if gp < 0 or gp > 7 or (val != OFF and val != ON): # Check the input parameters
            return        
        
        reg_val = self.read_register(GPINTEN) # Read the current status of the register
        if val == OFF:                      # Interrupt disabled on GPIO pin
            reg_val &= ~(1 << gp)
        else:                               # Interrupt is enabled on GP pin
            reg_val |= 1 << gp
        self.write_register(GPINTEN, reg_val) # Write the updated value of the register
    
    
    def gp_pullup(self, gp, val):
        if gp < 0 or gp > 7 or (val != OFF and val != ON): # Check the input parameters
            return        
        
        reg_val = self.read_register(GPPU)  # Read the current status of the register
        if val == OFF:                      # No pull-up on GPIO pin
            reg_val &= ~(1 << gp)
        else:                               # Pull-up is enabled on GPIO pin
            reg_val |= 1 << gp
        self.write_register(GPPU, reg_val)  # Write the updated value of the register        


    def gp_get_value(self, gp):
        if gp < 0 or gp > 7:                # Check the input parameter
            return        
        
        return (self.read_register(GPIO) >> gp) & 1 # Read the current status, shift and mask out
        

    def gp_set_value(self, gp, val):
        if gp < 0 or gp > 7 or (val != OFF and val != ON): # Check the input parameters
            return        
        
        reg_val = self.read_register(GPIO)  # Read the current status of the register
        if val == OFF:                      # Set GP pin low
            reg_val &= ~(1 << gp)
        else:                               # Set GP pin high
            reg_val |= 1 << gp
        self.write_register(GPIO, reg_val)  # Write the updated value of the register
    
    
# EOF #####################################################################
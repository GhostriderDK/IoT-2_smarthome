# EDUCABOARD ESP32 HARDWARE

# LCD
pin_lcd_rs        = 27
pin_lcd_enable    = 25
pin_lcd_db4       = 33
pin_lcd_db5       = 32
pin_lcd_db6       = 21
pin_lcd_db7       = 22

pin_lcd_contrast  = 23

lcd_num_lines     =  4
lcd_num_columns   = 20
              
# LED1
pin_led1          = 26

# TEMPERATURE LMT84
pin_temp          = 35
              
# POTMETER              
pin_potmeter      = 34
              
# PUSH BUTTONS
pin_pb1           =  4
pin_pb2           =  0

# ROTARY ENCODER, the pushbutton is connected to the port expander
pin_enc_a         = 39
pin_enc_b         = 36

# EEPROM
pin_eeprom_scl    = 18 # Not used directly but via I2C H/W 0 bus
pin_eeprom_sda    = 19 # Not used directly but via I2C H/W 0 bus

i2c_eeprom_hwbus  =  0 # I2C 0

# SPI
pin_portexp_miso  = 12 # Not used directly but via HSPI bus
pin_portexp_mosi  = 13 # Not used directly but via HSPI bus
pin_portexp_scl   = 14 # Not used directly but via HSPI bus
pin_portexp_cs    = 15
pin_portexp_int   =  2

spi_portexp_hwbus =  1 # SPI 1 = HSPI

# UART
pin_uart_rx       = 16 # Not used directly but via UART
pin_uart_tx       = 17 # Not used directly but via UART
pin_gps_pps       =  5

uart_gps_hw       =  2 # UART 2

# EOF #################################################################
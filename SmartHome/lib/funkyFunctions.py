# This is a collection of funky functions that many come in handy from time to time
#

#####################################################################################
# Bit manipulation and checking functions
#
#   Input
#       val: the value to manipulate/check
#       pos: the position to manipulate/check
#            For all functions it applies that a negative position (pos) will shift right
#   Output
#       The manipulated/checked value

def set_bit(val, pos):
    return val | (1 << pos)


def clear_bit(val, pos):
    return val & (~(1 << pos))


def toggle_bit(val, pos):
    return val ^ (1 << pos)


def check_bit(val, pos):
    return val & (1 << pos)  # no right justification so just check if equal to zero (0)


#####################################################################################
# Finds the day of the week 
#
#    Input
#        year : the year
#        month: the month
#        day  : the day
#    Output
#        A number telling the day, 0 = Monday, ... 6: Sunday
#
def day_of_week(year, month, day):
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    
    if (month < 3):
        year = year - 1
    
    return (year + int(year / 4) - int(year / 100) + int(year / 400) + t[month - 1] + day) % 7


#####################################################################################
# "Pings" an I2C address
#
#    Input
#        i2c_bus: the I2C bus object
#        addr   : the I2C address to "ping"
#    Output
#        True if a device is found otherwise False

def i2c_ping(i2c_bus, addr):
    try:
        i2c_bus.readfrom(addr, 0)
        return True
    except:
        return False


#####################################################################################
# Find the nearest upper power of any base, e.g. 4711 -> 10^4, 2^13
#
#    Input
#        base: the base value
#        exp : the exponent value
#    Output
#        The value of the nearest upper power

def nearest_upper_power(base, exp):
    if (base < exp):
        return 0
    elif (exp == 10):
        return ceil(log10(base))
    else:
        return ceil(log(base) / log(exp))


#####################################################################################
# Converts UTC to local time including daylight saving time
#
#    Input
#        utc_year            : the UTC year, YYYY
#        utc_month           : the UTC month
#        utc_day             : the UTC day
#        utc_hours           : the UTC hours
#        utc_minutes         : the UTC minutes
#        utc_seconds         : the UTC seconds
#        offset_hours        : the UTC to local offset hours, west is negative
#        offset_minutes      : the UTC to local offset minutes, always positive
#        daylight_saving_time: False if no daylight saving time, True if daylight saving time is used
#
#    Output
#        local_year, local_month, local_day, local_hours, local_minutes, local_seconds

def utc_to_local(utc_year, utc_month, utc_day, utc_hours, utc_minutes, utc_seconds, offset_hours = 0, offset_minutes = 0, daylight_saving_time = False):
        
    local_year = utc_year
    local_month = utc_month
    local_day = utc_day
    local_hours = utc_hours
    local_minutes = utc_minutes             # Local seconds are the same as UTC seconds

    if (offset_hours != 0) or (offset_minutes != 0) or (daylight_saving_time == True):
        
        # Handle February leap years
        days_i_month= [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if (utc_year % 4 == 0):                     # Centuries are not handled but less of a problem. Next time is 2100
            days_i_month[1] = 29

        # Find the total number of offset minutes 
        local_offset_minutes = 60 * offset_hours
        if offset_hours < 0:
            local_offset_minutes -= offset_minutes   # The offset hours carries the sign. The minutes are always positive
        else:
            local_offset_minutes += offset_minutes
            
        local_time = 60 * utc_hours + utc_minutes + local_offset_minutes

        # Handle daylight saving time
        if (daylight_saving_time):
            local_time += 60

        # The day before
        if (local_time < 0):                    
            local_time += 1440

            if (utc_day == 1):
                if (utc_month == 1):
                    local_year = utc_year - 1
                    local_month = 12
                else:
                    local_year = utc_year;
                local_month = utc_month - 1

                local_day = days_i_month[local_month - 1]
            else:
                local_year = utc_year
                local_month = utc_month
                local_day = utc_day - 1

        # The next day
        elif (local_time >= 1440):                 

            local_time -= 1440
            
            if (utc_day == days_i_month[utc_month - 1]):
                if (utc_month == 12):
                    local_year = utc_year + 1
                    local_month = 1
                else:
                    local_year = utc_year
                    local_month = utc_month + 1
                local_day = 1
            else:
                local_year = utc_year
                local_month = utc_month
                local_day = utc_day + 1
    
        local_hours = int(local_time / 60)
        local_minutes = local_time % 60

    return local_year, local_month, local_day, local_hours, local_minutes, utc_seconds # Local seconds are the same as UTC seconds

# EOF ################################################################################

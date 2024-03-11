import time

from scd4x_sensirion import SCD4xSensirion
from machine import I2C, Pin
from sensor_pack.bus_service import I2cAdapter


if __name__ == '__main__': 
    i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)
    adaptor = I2cAdapter(i2c)
    # sensor
    sen = SCD4xSensirion(adaptor)
    # Force return sensor in IDLE mode!
    sen.set_measurement(start=False, single_shot=False)
    sid = sen.get_id()
    print(f"Sensor id 3 x Word: {sid[0]:x}:{sid[1]:x}:{sid[2]:x}")
    # t_offs = 0.0
    # Warning: To change or read sensor settings, the SCD4x must be in idle mode!!!
    # Otherwise an EIO exception will be raised!
    # print(f"Set temperature offset sensor to {t_offs} Celsius")
    # sen.set_temperature_offset(t_offs)
    t_offs = sen.get_temperature_offset()
    print(f"Get temperature offset from sensor: {t_offs} Celsius")
    masl = 68  # Meter Above Sea Level
    print(f"Set my place M.A.S.L. to {masl} meter")
    sen.set_altitude(masl)
    masl = sen.get_altitude()
    print(f"Get M.A.S.L. from sensor: {masl} meter")
    # data ready
    if sen.is_data_ready():
        print("Measurement data can be read!")  # Данные измерений могут быть прочитаны!
    else:
        print("Measurement data missing!")
    
    if sen.is_auto_calibration():
        print("The automatic self-calibration is ON!")
    else:
        print("The automatic self-calibration is OFF!")

    sen.set_measurement(start=True, single_shot=False)      # periodic start
    wt = sen.get_conversion_cycle_time()
    print(f"conversion cycle time [ms]: {wt}")
    print("Periodic measurement started")
    repeat = 5
    multiplier = 2
    for i in range(repeat):
        time.sleep_ms(wt)
        co2, t, rh = sen.get_meas_data()
        print(f"CO2 [ppm]: {co2}; T [°C]: {t}; RH [%]: {rh}")
    
    print(20*"*_")
    print("Reading using an iterator!")
    for counter, items in enumerate(sen):
        time.sleep_ms(wt)
        if items:
            co2, t, rh = items
            print(f"CO2 [ppm]: {co2}; T [°C]: {t}; RH [%]: {rh}")
            if repeat == counter:
                break

    print(20 * "*_")
    print("Using single shot mode!")
    # Force return sensor in IDLE mode!
    sen.set_measurement(start=False, single_shot=False)
    cnt = 0
    while True:
        sen.set_measurement(start=False, single_shot=True, rht_only=False)
        time.sleep_ms(multiplier * wt)      # 3x period
        co2, t, rh = sen.get_meas_data()
        print(f"CO2 [ppm]: {co2}; T [°C]: {t}; RH [%]: {rh}")
        cnt += 1
        if cnt > repeat:
            break

    # sen.set_measurement(start=False, single_shot=False)
    sen.set_measurement(start=False, single_shot=True, rht_only=True)   # rht only mode!
    wt = sen.get_conversion_cycle_time()
    print(20 * "*_")
    # Использование режима измерения по запросу! Только относительная влажность и температура измеряются датчиком!
    # относительная влажность + температура. CO2 всегда равна нулю или не изменяется!!
    print("Using single shot mode! RH + T only! (Temp + RH. CO2 always zero or does not change!!)")
    while True:
        time.sleep_ms(multiplier * wt)      # 3x period
        co2, t, rh = sen.get_meas_data()
        print(f"CO2 [ppm]: {co2}; T [°C]: {t}; RH [%]: {rh}")
        sen.set_measurement(start=False, single_shot=True, rht_only=True)   # rht only mode!

from machine import UART
from utime import sleep

print("###  PM1006K Particle sensor  ###")
uart1 = UART(2, baudrate=9600)


def valid_header(d):
    print("data = " + str(d) + "\n")
    headerValid = (d[0] == 0x16 and d[1] == 0x11 and d[2] == 0x0B)
    if headerValid:
        print("msg header valid\n")
    else:
        print("msg header not valid\n")
    return headerValid



while True:
    uart1.write(b"11 01 02 EC")
    data = uart1.read(32)
    print(data)
    if data is not None:
        v = valid_header(data)
        print("v = " + str(v) +"\n")
    else:
        print("data is NONE\n")
    sleep(10)

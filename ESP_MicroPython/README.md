# KEA IT-Teknolog IOT2 projekt
## IndeklimaKontrol ESP32 Micropython kode

Dette er koden der ligger på ESP32 modulerne.
boot.py starter iot_main.py eller iot_dht11.py, afhængig af hvilken type enhed.

Vi har anvendt følgende libraries:
* [micropython-mqtt](https://github.com/peterhinch/micropython-mqtt/) asynchronous MQTT driver af Peter Hinch
* [SCD40x](https://github.com/octaprog7/SCD4x) af Roman/octaprog7
* [ENS160](https://github.com/octaprog7/ens160) af Roman/octaprog7  
* ADC_substitute af Bo Hansen

For at interface lettere med nogle af de libraries vi har brugt, har vi lavet iot_scd40.py og ens160.py, der gør de funktioner vi bruger tilgængelige.
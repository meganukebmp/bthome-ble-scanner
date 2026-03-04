# BTHome BLE Scanner
This is a python program that scans for BTHome devices and lists them out sorted by RSSI
As an optional parameter you can pass the MAC of the device, then the program will listen to that specific device and show the advertised data in a structured way.
Its primary usecase is debugging new BTHome devices

### Usage:
```
python scanner.py
# or
python scanner.py 11:22:33:AA:BB:CC
```

### Example output:
```
RSSI|LAST S| BLUETOOTH MAC     | Device Name
-62 |   63 | 11:22:33:AA:BB:C1 | My Device
-66 |    5 | 11:22:33:AA:BB:C2 | Other Device
-78 |    9 | 11:22:33:AA:BB:C3 | Other Device
-82 |    5 | 11:22:33:AA:BB:C4 | Other Device 
```

And

```
RSSI|LAST S| BLUETOOTH MAC     | Device Name
-78 |   34 | 11:22:33:AA:BB:C3 | Other Device <-- Button
packet_id: 5
button: 1
moisture: 0
temperature: 27.0
count_16: 6112
battery: 93
RAW REPORT: 40 00 05 3A 01 2F 00 02 8C 0A 3D E0 17 01 5DB
```

Values that have updated or changed flash in green.

### Wants:
- BTHome flags processing
- Ability to copy paste (or interractive UI entirely)
- Graphing of interest values over time
- Exporting interest values over time to CSV
- The ability to see and parse other GATT characteristics
- Pairing mode indication
- Encryption handling
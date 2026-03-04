import asyncio
import curses
import sys
import signal
from bleak import BleakScanner
import struct
from parser import decode_ha_ble_packet
from datetime import datetime
from netaddr import EUI, mac_unix_expanded

BTHOME_UUID = "0000fcd2-0000-1000-8000-00805f9b34fb"

seen = {}
device_mac = ""
filter_mac = False
old_data = {}

def signal_handler(sig, frame):
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    sys.exit(0)

def print_usage():
    print(f"Usage: {sys.argv[0]} [OPTIONAL: MAC]")

def is_mac_address(mac):
    try:
        # parse mac
        e = EUI(mac)
        # 00:11:22:33:44:55
        e.dialect = mac_unix_expanded
        return True
    except:
        return False

def callback(device, advertisement_data):
    if filter_mac and device.address != device_mac:
        return
    if advertisement_data is not None:
        if getattr(advertisement_data, "service_data", None):
            for uuid, payload in advertisement_data.service_data.items():
                if uuid == BTHOME_UUID:
                    seen[device.address] = {
                        "rssi": advertisement_data.rssi,
                        "name": device.name,
                        "readings": decode_ha_ble_packet(payload),
                        "changed": True,
                        "last_seen": 0,
                        "raw": payload
                    }


async def main(stdscr):
    signal.signal(signal.SIGINT, signal_handler)

    global seen
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    scanner = BleakScanner(detection_callback=callback)
    await scanner.start()

    while True:
        await asyncio.sleep(1)

        seen = dict(sorted(seen.items(), key=lambda x: x[1]['rssi'], reverse=True))
        
        stdscr.clear()

        stdscr.addstr(0, 0, "RSSI|LAST S| BLUETOOTH MAC     | Device Name")

        y = 1
        for address, data in seen.items():
            button = False
            if "button" in data["readings"]:
                if data["readings"]["button"] != 0:
                    button = True

            info = f"{data["rssi"]:>3} | {data["last_seen"]:>4} | {address} | {data["name"] or "None"} {"<-- Button" if button else ""}"

            if data["changed"]:
                if button:
                    stdscr.addstr(y, 0, info, curses.color_pair(2))
                else:
                    stdscr.addstr(y, 0, info, curses.color_pair(1))
            else:
                stdscr.addstr(y, 0, info)

            if filter_mac:
                y = 1
                changed_keys = []
                for key, value in data["readings"].items():
                    if key in old_data:
                        if old_data[key] != value:
                            changed_keys.append(key)
                    old_data[key] = value

                    y+=1

                y = 2
                for key, value in old_data.items():
                    val = f"{key}: {value}"
                    if key in changed_keys:
                        stdscr.addstr(y, 0, val, curses.color_pair(1))
                    else:
                        stdscr.addstr(y, 0, val)
                    y+=1

                raw = "RAW REPORT: "
                for b in data["raw"]:
                    raw = raw + f"{b:02X} "
                if data["changed"]:
                    stdscr.addstr(y, 0, raw, curses.color_pair(1))
                else:
                    stdscr.addstr(y, 0, raw)


            data["changed"] = False
            data["last_seen"] = data["last_seen"] + 1
            y+=1
        stdscr.refresh()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print_usage()
        sys.exit(0)
    if len(sys.argv) == 2:
        if not is_mac_address(sys.argv[1]):
            print("Not a valid MAC format!")
            print_usage()
            sys.exit(0)
        device_mac = sys.argv[1].upper()
        filter_mac = True
    
    asyncio.run(curses.wrapper(main))
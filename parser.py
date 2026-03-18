import struct

# HA BLE types ID (name, type, bytesize, scale)
HA_BLE_TYPES = {
    0x00: ("packet_id", "uint8", 1, 1),
    0x01: ("battery", "uint8", 1, 1),
    0x02: ("temperature", "sint16", 2, 0.01),
    0x03: ("humidity_f", "uint16", 2, 0.01),
    0x04: ("pressure", "uint24", 3, 0.01),
    0x05: ("illuminance", "uint24", 3, 0.01),
    0x06: ("mass_kg", "uint16", 2, 0.01),
    0x07: ("mass_lb", "uint16", 2, 0.01),
    0x08: ("dewpoint", "sint16", 2, 0.01),
    0x09: ("count", "uint8", 1, 1),
    0x0A: ("energy", "uint24", 3, 0.001),
    0x0B: ("power", "uint24", 3, 0.01),
    0x0C: ("voltage", "uint16", 2, 0.001),
    0x0D: ("pm2_5", "uint16", 2, 1),
    0x0E: ("pm10", "uint16", 2, 1),
    0x0F: ("generic_boolean", "uint8", 1, 1),
    0x10: ("power_bool", "uint8", 1, 1),
    0x11: ("opening", "uint8", 1, 1),
    0x12: ("co2", "uint16", 2, 1),
    0x13: ("tvoc", "uint16", 2, 1),
    0x14: ("moisture_f", "uint16", 2, 0.01),
    0x15: ("battery_low", "uint8", 1, 1),
    0x16: ("battery_charging", "uint8", 1, 1),
    0x17: ("carbon_monoxide", "uint8", 1, 1),
    0x18: ("cold", "uint8", 1, 1),
    0x19: ("connectivity", "uint8", 1, 1),
    0x1A: ("door", "uint8", 1, 1),
    0x1B: ("garage_door", "uint8", 1, 1),
    0x1C: ("gas", "uint8", 1, 1),
    0x1D: ("heat", "uint8", 1, 1),
    0x1E: ("light", "uint8", 1, 1),
    0x1F: ("lock", "uint8", 1, 1),
    0x20: ("moisture_bool", "uint8", 1, 1),
    0x21: ("motion", "uint8", 1, 1),
    0x22: ("moving", "uint8", 1, 1),
    0x23: ("occupancy", "uint8", 1, 1),
    0x24: ("plug", "uint8", 1, 1),
    0x25: ("presence", "uint8", 1, 1),
    0x26: ("problem", "uint8", 1, 1),
    0x27: ("running", "uint8", 1, 1),
    0x28: ("safety", "uint8", 1, 1),
    0x29: ("smoke", "uint8", 1, 1),
    0x2A: ("sound", "uint8", 1, 1),
    0x2B: ("tamper", "uint8", 1, 1),
    0x2C: ("vibration", "uint8", 1, 1),
    0x2D: ("window", "uint8", 1, 1),
    0x2E: ("humidity", "uint8", 1, 1),
    0x2F: ("moisture", "uint8", 1, 1),
    0x3A: ("button", "uint8", 1, 1),
    0x3C: ("dimmer", "uint8", 1, 1),
    0x3D: ("count_16", "uint16", 2, 1),
    0x3E: ("count_32", "uint32", 4, 1),
    0x3F: ("rotation", "sint16", 2, 0.1),
    0x40: ("distance_mm", "uint16", 2, 1),
    0x41: ("distance_m", "uint16", 2, 0.1),
    0x42: ("duration", "uint24", 3, 0.001),
    0x43: ("current", "uint16", 2, 0.001),
    0x44: ("speed", "uint16", 2, 0.01),
    0x45: ("temperature_hi", "sint16", 2, 0.1),
    0x46: ("uv_index", "uint8", 1, 0.1),
    0x50: ("timestamp", "uint32", 4, 1),
    0x53: ("text", "string", None, 1),
    0x54: ("raw", "bytes", None, 1),
    0x59: ("count_i8", "sint8", 1, 1),
    0x5A: ("count_i16", "sint16", 2, 1),
    0x5B: ("count_i32", "sint32", 4, 1),
    0x5E: ("direction", "uint16", 2, 0.01),
    0x5F: ("precipitation", "uint16", 2, 1),
    0x64: ("light_level", "uint8", 1, 1),
    0xF0: ("device_type_id", "uint16", 2, 1),
    0xF1: ("fw_version_long", "uint32", 4, 1),
    0xF2: ("fw_version_short", "uint24", 3, 1),
}

# TODO add flags

def read_sint8(data, offset):
    val = struct.unpack_from("<b", data, offset)[0]
    return val, offset + 1

def read_uint8(data, offset):
    val = struct.unpack_from("<B", data, offset)[0]
    return val, offset + 1

def read_sint16(data, offset):
    val = struct.unpack_from("<h", data, offset)[0]
    return val, offset + 2

def read_uint16(data, offset):
    val = struct.unpack_from("<H", data, offset)[0]
    return val, offset + 2

def read_uint24(data, offset):
    # for 24 bits read 3 times and combine
    b1, b2, b3 = struct.unpack_from("<BBB", data, offset)
    val = b1 | (b2 << 8) | (b3 << 16)
    return val, offset + 3

def read_uint32(data, offset):
    val = struct.unpack_from("<I", data, offset)[0]
    return val, offset + 4

def read_sint32(data, offset):
    val = struct.unpack_from("<i", data, offset)[0]
    return val, offset + 4

def read_string(data, offset):
    size = data[offset]
    val = data[offset+1:offset+1+size].decode("utf-8")
    return val, offset + size + 1

def read_bytes(data, offset):
    size = data[offset]
    raw = data[offset+1:offset+1+size]
    val = " ".join(f"{b:02X}" for b in raw)
    return val, offset + size + 1

TYPE_READERS = {
    "uint8": read_uint8,
    "sint8": read_sint8,
    "sint16": read_sint16,
    "uint16": read_uint16,
    "uint24": read_uint24,
    "uint32": read_uint32,
    "sint32": read_sint32,
    "string": read_string,
    "bytes": read_bytes,
}

def decode_ha_ble_packet(raw_bytes):
    # start from 1 since byte 0 is flags
    offset = 1
    decoded = {}
    
    while offset < len(raw_bytes):
        type_id = raw_bytes[offset]
        offset += 1
        
        if type_id not in HA_BLE_TYPES:
            print(f"Unknown type ID: {type_id:02x}")
            for b in raw_bytes:
                print(f"{b:02x}")
            break
        
        name, data_type, size, scale = HA_BLE_TYPES[type_id]
        value, offset = TYPE_READERS[data_type](raw_bytes, offset)
        if scale == 0:
            decoded[name] = value
        else:
            decoded[name] = value * scale

    return decoded
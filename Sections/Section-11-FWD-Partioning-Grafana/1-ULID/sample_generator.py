import uuid
import time
import base64
import base58
import ulid
from uuid import UUID

def uuid_v7():
    return UUID(bytes=b'\x07' + int(time.time() * 1000).to_bytes(6, 'big') + uuid.uuid4().bytes[7:])

def base32_encode(uuid_obj):
    return base64.b32encode(uuid_obj.bytes).decode('ascii').rstrip('=')

def base58_encode(uuid_obj):
    return base58.b58encode(uuid_obj.bytes).decode('ascii')

# Auto-increment
auto_increment = 1000000000000000000
print(f"Auto-increment: {auto_increment}")
print(f"Next Auto-increment: {auto_increment + 1}\n")

# UUID v4
uuid_v4 = uuid.uuid4()
print(f"UUID v4: {uuid_v4}")
print(f"UUID v4 (hex): {uuid_v4.hex}\n")

# UUID v7
uuid_v7_sample = uuid_v7()
print(f"UUID v7: {uuid_v7_sample}")
print(f"UUID v7 (hex): {uuid_v7_sample.hex}")

# UUID v7 Base32
uuid_v7_base32 = base32_encode(uuid_v7_sample)
print(f"UUID v7 Base32: {uuid_v7_base32}")

# UUID v7 Base58
uuid_v7_base58 = base58_encode(uuid_v7_sample)
print(f"UUID v7 Base58: {uuid_v7_base58}")

# UUID v7 Binary
uuid_v7_binary = uuid_v7_sample.bytes
print(f"UUID v7 Binary: {uuid_v7_binary}")
print(f"UUID v7 Binary (hex): {uuid_v7_binary.hex()}\n")

# ULID
ulid_sample = ulid.new()
print(f"ULID: {ulid_sample}")
print(f"ULID (bytes): {ulid_sample.bytes}")

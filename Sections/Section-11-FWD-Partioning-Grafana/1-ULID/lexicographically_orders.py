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

def generate_sequential_ids(num_ids=5):
    print("Auto-increment:")
    auto_increment = 1000000000000000000
    for i in range(num_ids):
        print(f"{auto_increment + i}")
    print()

    print("UUID v4:")
    for _ in range(num_ids):
        print(f"{uuid.uuid4()}")
    print()

    print("UUID v7:")
    for _ in range(num_ids):
        time.sleep(0.001)  # Small delay to ensure different timestamps
        print(f"{uuid_v7()}")
    print()

    print("UUID v7 Base32:")
    for _ in range(num_ids):
        time.sleep(0.001)
        print(f"{base32_encode(uuid_v7())}")
    print()

    print("UUID v7 Base58:")
    for _ in range(num_ids):
        time.sleep(0.001)
        print(f"{base58_encode(uuid_v7())}")
    print()

    print("UUID v7 Binary (hex representation):")
    for _ in range(num_ids):
        time.sleep(0.001)
        print(f"{uuid_v7().bytes.hex()}")
    print()

    print("ULID:")
    for _ in range(num_ids):
        time.sleep(0.001)
        print(f"{ulid.new()}")
    print()

generate_sequential_ids()
from smbus2 import SMBus

# Replace 0x27 with the actual I2C address of your device
address = 0x27

with SMBus(1) as bus:
    bus.write_byte(address, 0x01)
print(bus)
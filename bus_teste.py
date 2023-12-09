from smbus2 import SMBus

# Replace 0x27 with the actual I2C address of your device
address = 0x27

bus = SMBus(1)
print(bus)
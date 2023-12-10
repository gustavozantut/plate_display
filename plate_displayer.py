from confluent_kafka import Consumer, KafkaError
from pyfirmata import Arduino, util
import time
import json
import smbus

arduino_port = '/dev/ttyACM0'
board = Arduino(arduino_port)
it = util.Iterator(board)
it.start()
# Define I2C LCD configuration
lcd_i2c_address = 0x27  # Adjust the address based on your I2C LCD module
lcd_columns = 16
lcd_rows = 2

kafka_config = {
    'bootstrap.servers': '192.168.0.101:9092,192.168.14.2:9092,192.168.14.2:9093',
    'group.id': 'plate_displayer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_config)
consumer.subscribe(['plate_detector'])

def display_on_lcd(i2c_address=0x27, message="XXXXXXX"):
    # Create an smbus object
    bus = smbus.SMBus(1)  # Use 0 for older Raspberry Pi boards

    # I2C LCD configuration
    lcd_control = 0x08  # Control byte for LCD
    lcd_data = 0x40     # Data byte for LCD

    # Define function set command for 4-bit mode
    fs_command = 0b00101000  # Function Set: 4-bit mode, 2 lines, 5x8 font
    bus.write_byte_data(i2c_address, lcd_control, fs_command)

    # Define entry mode command
    em_command = 0b00000110  # Entry Mode Set: Increment cursor, no display shift
    bus.write_byte_data(i2c_address, lcd_control, em_command)

    # Clear the LCD
    bus.write_byte_data(i2c_address, lcd_control, 0x01)
    time.sleep(0.1)  # Wait for the clear command to complete

    # Display the message on the LCD
    for char in message:
        lcd_byte = ord(char)
        bus.write_i2c_block_data(i2c_address, lcd_data, [lcd_byte, 0b00010000])  # High nibble, RS = 1
        bus.write_i2c_block_data(i2c_address, lcd_data, [lcd_byte << 4, 0b00010000])  # Low nibble, RS = 1
        time.sleep(0.01)  # Short delay between characters

    # Wait for a moment to view the message (adjust as needed)
    time.sleep(2)

    # Clear the LCD again
    bus.write_byte_data(i2c_address, lcd_control, 0x01)
    time.sleep(0.1)

try:
    
    while True:
        
        msg = consumer.poll(1.0)

        if msg is None:
            
            continue
        
        if msg.error():
            
            if msg.error().code() == KafkaError._PARTITION_EOF:
                
                continue
            
            else:
                
                print(msg.error())
                break

        lcd_message = msg.value().decode('utf-8')
        lcd_message = json.loads(lcd_message)
        lcd_message = lcd_message["results"][0]["plate"]
        print(f"sending plate {lcd_message} to ino")
        display_on_lcd(message=lcd_message)
        print(f"plate sent")

except KeyboardInterrupt:
    
    pass

finally:
    
    consumer.close()
    board.exit()
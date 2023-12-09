from confluent_kafka import Consumer, KafkaError
from pyfirmata import Arduino, util
import time
import json

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

def display_on_lcd(arduino=arduino_port, i2c_address=lcd_i2c_address, lcd_columns=lcd_columns, lcd_rows=lcd_rows, message="XXXXXXX"):
    # Define I2C LCD configuration
    lcd = arduino.I2C(i2c_address, lcd_columns, lcd_rows)

    # Clear the LCD
    lcd.write("\x01")  # 0x01 is the ASCII control code for Clear Display

    # Display the message on the LCD
    lcd.write(message)

    # Wait for a moment to view the message (adjust as needed)
    time.sleep(2)

    # Clear the LCD again
    lcd.write("\x01")

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
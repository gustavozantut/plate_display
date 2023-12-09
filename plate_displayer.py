from confluent_kafka import Consumer, KafkaError
import serial
import time

arduino_port = '/dev/ttyACM0'
arduino_code_path = './lcd_displayer.ino'

kafka_config = {
    'bootstrap.servers': '192.168.0.101:9092,192.168.14.2:9092,192.168.14.2:9093',
    'group.id': 'plate_displayer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_config)
consumer.subscribe(['plate_detector'])

ser = serial.Serial(arduino_port, 9600, timeout=5)

def upload_and_run_code(code):
    
    ser.write(b'U')
    time.sleep(2)
    ser.write(code.encode())
    ser.write(b'R')

def display_on_lcd(message):
    
    ser.write(b'U')  # Upload code to Arduino
    time.sleep(2)
    code_to_display = f'displayOnLCD("{message}")'
    ser.write(code_to_display.encode())
    ser.write(b'R')  # Run the code to display on LCD

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
        print(lcd_message)
        display_on_lcd(lcd_message["results"]["plate"])

except KeyboardInterrupt:
    
    pass

finally:
    
    consumer.close()
    ser.close()
from confluent_kafka import Consumer, KafkaError
import time
import json
import serial

arduino_port = '/dev/ttyACM0'
ser = serial.Serial(arduino_port, 9600, timeout=5)

kafka_config = {
    'bootstrap.servers': '192.168.0.101:9092,192.168.14.2:9092,192.168.14.2:9093',
    'group.id': 'plate_displayer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_config)
consumer.subscribe(['plate_detector'])

def display_on_lcd(message="XXXXXXX"):
    
    ser.write(message.encode())
    time.sleep(1)  # Add a delay if necessary

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
        lcd_message = '      '+lcd_message["results"][0]["plate"]
        print(f"sending plate {lcd_message} to ino")
        display_on_lcd(message=lcd_message)
        print(f"plate sent")

except KeyboardInterrupt:
    
    pass

finally:
    
    consumer.close()
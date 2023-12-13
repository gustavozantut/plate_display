from confluent_kafka import Consumer, KafkaError
import time
import json
import serial
import logging

def configure_logging():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a file handler
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

arduino_port = '/dev/ttyACM1'
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
    time.sleep(0.5)  # Add a delay if necessary

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
        lcd_message = '     '+lcd_message["results"][0]["plate"]+'\n'
        logging.info(f"sending plate {lcd_message} to ino")
        display_on_lcd(message=lcd_message)
        logging.info(f"plate sent")

except KeyboardInterrupt:
    
    pass

finally:
    
    consumer.close()
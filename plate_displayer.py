from RPLCD.i2c import CharLCD
from confluent_kafka import Consumer, KafkaError
import time
import json

# Initialize LCD with I2C address 0x27
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, backlight_enabled=True)

# Kafka Consumer configuration
consumer_conf = {
    'bootstrap.servers': '192.168.0.101:9092,192.168.14.2:9092,192.168.14.2:9093',
    'group.id': 'plate_displayer',
    'auto.offset.reset': 'earliest'
}

# Create Kafka Consumer
consumer = Consumer(consumer_conf)

# Subscribe to the Kafka topic
consumer.subscribe(['plate_detector'])

try:
    
    while True:
        
        # Poll for messages
        msg = consumer.poll(timeout=1000)  # Adjust the timeout as needed

        if msg is None:
            
            continue
        
        if msg.error():
            
            if msg.error().code() == KafkaError._PARTITION_EOF:
                
                # End of partition event, not an error
                continue
            
            else:
                
                print(msg.error())
                break

        # Decode and display the license plate
        try:
            
            plate_info = json.loads(msg.value().decode('utf-8'))
            plate = plate_info["results"]["plate"]

            # Display the license plate on the LCD
            lcd.clear()
            lcd.write_string("License Plate:")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(plate)

            # Wait for a few seconds
            time.sleep(1)

        except json.JSONDecodeError as e:
            
            continue

except KeyboardInterrupt:
    
    pass

finally:
    
    # Close the Kafka Consumer
    consumer.close()
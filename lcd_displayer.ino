#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // Set the I2C address and LCD dimensions

void setup() {
  lcd.begin(16, 2);  // Initialize the LCD
  lcd.print("LCD Ready");  // Display a startup message
  delay(2000);

  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  if (Serial.available() > 0) {
    String message = readSerialMessage();
    displayOnLCD(message);
  }
}

String readSerialMessage() {
  String message = "";
  while (Serial.available() > 0) {
    char c = Serial.read();
    message += c;
    delay(10);  // Small delay to allow complete message reception
  }
  return message;
}

void displayOnLCD(String message) {
  lcd.clear();
  lcd.print(message);
}
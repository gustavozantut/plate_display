#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // Set the I2C address and LCD dimensions

void setup() {
  lcd.init();
  lcd.setBacklight(HIGH);
  lcd.setCursor(0,0);
  lcd.print("     PISTA 1");  // Display "PISTA 1" on the first line
  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  if (Serial.available() > 0) {
    String receivedMessage = Serial.readStringUntil('\n');  // Read the entire message until newline
    lcd.setCursor(0, 1);  // Move to the second line
    lcd.print(receivedMessage);  // Display the received message on the second line
  }
}
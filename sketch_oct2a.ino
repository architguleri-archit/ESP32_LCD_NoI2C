#include <LiquidCrystal.h>

// RS, E, D4, D5, D6, D7 connected to ESP32
LiquidCrystal lcd(21, 22, 18, 19, 23, 5);

void setup() {
  lcd.begin(16, 2);           // Initialize 16x2 LCD
  lcd.print("Hello, ESP32!"); // Print on first line
  lcd.setCursor(0, 1);        // Move to 2nd line
  lcd.print("No I2C Module");
}

void loop() {
  // Nothing here
}


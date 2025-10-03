#include <LiquidCrystal.h>

// RS, E, D4, D5, D6, D7
LiquidCrystal lcd(21, 22, 18, 19, 23, 5);

const int lcdWidth = 16;
const int lcdHeight = 2;
const int ledPin = 2;  // On-board LED (ESP32)

// Title text
String line1 = "THANKS";
String line2 = "FOR WATCHING";

// Define smiley face
void defineCustomChars() {
  byte smiley[8] = {
    0b00000,
    0b01010,
    0b01010,
    0b00000,
    0b00000,
    0b10001,
    0b01110,
    0b00000
  };
  lcd.createChar(6, smiley);
}

// Clear a line
void clearLine(int line) {
  lcd.setCursor(0, line);
  lcd.print(F("                "));
  lcd.setCursor(0, line);
}

// Boot animation
void bootAnimation() {
  int totalSteps = 100;
  int lcdDelay = 80;
  int ledState = LOW;
  unsigned long lastBlink = 0;

  clearLine(0);
  clearLine(1);

  for (int percent = 0; percent <= totalSteps; percent++) {
    int charsToFill = (percent * lcdWidth) / 100;

    // Progress bar
    lcd.setCursor(0, 0);
    for (int i = 0; i < lcdWidth; i++)
      lcd.write(i < charsToFill ? (uint8_t)255 : ' ');

    // Loading text
    lcd.setCursor(0, 1);
    lcd.print("Loading: ");
    if (percent < 10) lcd.print(" "); 
    lcd.print(percent);
    lcd.print("%   ");

    // LED blink faster as % increases
    int blinkInterval = map(percent, 0, totalSteps, 400, 50);
    if (millis() - lastBlink >= blinkInterval) {
      ledState = !ledState;
      digitalWrite(ledPin, ledState);
      lastBlink = millis();
    }

    delay(lcdDelay);
  }

  digitalWrite(ledPin, LOW);
  clearLine(0);
  clearLine(1);
}

// Typewriter "PLEASE SUBSCRIBE :)"
void typewriterRevealAnimation(int durationSeconds = 10) {
  String revealText = "PLEASE SUBSCRIBE "; 
  const int typingDelay = 150;

  clearLine(0); 
  clearLine(1);
  lcd.setCursor(0, 1);

  for (int i = 0; i < revealText.length() + 1; i++) {
    if (i == revealText.length()) {
      lcd.write(byte(6)); // smiley
    } else {
      lcd.print(revealText[i]);
    }
    delay(typingDelay);
  }

  unsigned long startTime = millis();
  while (millis() - startTime < durationSeconds * 1000UL) {
    if (millis() % 1000 < 500) { 
        digitalWrite(ledPin, HIGH);
    } else {
        digitalWrite(ledPin, LOW);
    }
  }
  digitalWrite(ledPin, LOW);
  clearLine(0); 
  clearLine(1);
}

void setup() {
  lcd.begin(lcdWidth, lcdHeight);
  pinMode(ledPin, OUTPUT);
  defineCustomChars();
  lcd.clear();
}

void loop() {
  // Boot sequence
  bootAnimation();
  lcd.clear();

  // Center text
  int startCol1 = (lcdWidth - line1.length()) / 2;
  int startCol2 = (lcdWidth - (line2.length() + 2)) / 2;

  // Alternating THANKS / FOR WATCHING
  for (int i = 0; i < 4; i++) {
    clearLine(1); 
    lcd.setCursor(startCol1, 0);
    lcd.print(line1);
    digitalWrite(ledPin, HIGH);
    delay(400);

    clearLine(0);
    lcd.setCursor(startCol2, 1);
    lcd.print(line2);
    lcd.print(" ");
    lcd.write(byte(6));
    digitalWrite(ledPin, LOW);
    delay(400);
  }

  // Final state (both lines)
  clearLine(0);
  lcd.setCursor(startCol1, 0);
  lcd.print(line1);

  clearLine(1);
  lcd.setCursor(startCol2, 1);
  lcd.print(line2);
  lcd.print(" ");
  lcd.write(byte(6));

  // Final typewriter message
  typewriterRevealAnimation(10);
}

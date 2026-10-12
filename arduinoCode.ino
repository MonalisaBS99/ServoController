#include <Servo.h>

Servo myServo;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);
  myServo.write(90);
  Serial.println("READY");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.length() > 0) {
      int angle = input.toInt();

      if (angle >= 0 && angle <= 180) {
        myServo.write(angle);
        Serial.print("OK: ");
        Serial.println(angle);
      }
    }
  }
}

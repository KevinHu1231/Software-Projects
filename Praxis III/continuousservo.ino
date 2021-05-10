#include <Servo.h>
Servo myservo;

void setup() {
  myservo.attach(10);
}

void loop() {
  myservo.write(180);
  delay(5000);
  myservo.write(92);

  delay(500);

  /*myservo.write(0);
  delay(5000);
  myservo.write(92);*/

  while(1){}
}

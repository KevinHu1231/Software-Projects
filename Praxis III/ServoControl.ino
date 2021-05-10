#include <Servo.h>
Servo myservo;
int pos = 0;
int incomingByte = 0;

void setup() {
  Serial.begin(9600);
  myservo.attach(10);
}

void loop() {
  if (Serial.available() > 0){
    incomingByte = Serial.read();
    Serial.print("received: ");
    Serial.print(incomingByte);
    if(incomingByte == 108){
      Serial.println("Left");
      myservo.write(0);
      delay(300);
      myservo.write(92);
    }else if (incomingByte == 114){
      Serial.println("Right");
      myservo.write(180);
      delay(300);
      myservo.write(92);
    }
    else{

    }
  }
}

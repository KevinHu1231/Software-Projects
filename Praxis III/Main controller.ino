#include <SoftwareSerial.h>
SoftwareSerial base_Serial(10,11); // RX | TX 

char base_input = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //Serial.println("Software Serial Mode: ");
  base_Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  base_Control();
}
void base_Control(){
  if (Serial.available()){
    base_input = Serial.read();
     Serial.println(base_input);
    if(base_input == 'a'|base_input== 'd'){
      
       base_Serial.write(base_input);
    }
   
  }
}

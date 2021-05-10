// Stepper motor for X 
int stepPin_x = 3; //  X
int dirPin_x = 2;   // for X 

int stepPin_z = 5; // Z
int dirPin_z = 4;   // Z 

char val = 0; //the input value 


void setup() {
  // put your setup code here, to run once:
  pinMode(stepPin_x,OUTPUT);
  pinMode(dirPin_x,OUTPUT);
  pinMode(stepPin_z,OUTPUT);
  pinMode(dirPin_z,OUTPUT);

  Serial.begin(9600);
  
}

void loop() {
/*     digitalWrite(dirPin_x,HIGH);
      for (int x=0; x<200;x++){
        digitalWrite(stepPin_x,HIGH);
        delayMicroseconds(2000);
        digitalWrite(stepPin_x,LOW);
        delayMicroseconds(2000);
       
      }
       delay(1000);
*/
  // put your main code here, to run repeatedly:
  
  if (Serial.available()){
    val = Serial.read();   // read the value of input 
    if (val == 'a'){   // x direction going left  
      digitalWrite(dirPin_x,HIGH);
      Serial.println(val);
      for (int x=0; x<200;x++){
        digitalWrite(stepPin_x,HIGH);
        delayMicroseconds(1000);
        digitalWrite(stepPin_x,LOW);
        delayMicroseconds(1000);
       
      }
       delay(500);
    }
    if (val == 'd'){    // x direction going right 
      digitalWrite(dirPin_x,LOW);
      for (int x=0; x<200;x++){
        digitalWrite(stepPin_x,HIGH);
        delayMicroseconds(1500);
        digitalWrite(stepPin_x,LOW);
        delayMicroseconds(1500);
       
      }
       delay(500);
    }
    
    if (val=='w'){ // z direction going up 
      digitalWrite(dirPin_z,HIGH);
      for(int x=0; x<200;x++){
        digitalWrite(stepPin_z,HIGH);
        delayMicroseconds(1500);
        digitalWrite(stepPin_z,LOW);
        delayMicroseconds(1500);
       
      }
       delay(500);
    }

    if (val=='s'){ // z direction going down 
      digitalWrite(dirPin_z,LOW);
      for(int x=0; x<200;x++){
        digitalWrite(stepPin_z,HIGH);
        delayMicroseconds(1500);
        digitalWrite(stepPin_z,LOW);
        delayMicroseconds(1500);
       
      }
       delay(500);
    }
  
   
  }

}

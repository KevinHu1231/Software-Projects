int Lmotorpin1 = 4;
int Lmotorpin2 = 5;
int Rmotorpin1 = 6;
int Rmotorpin2 = 7;
int trigPin1 = 8;
int trigPin2 = 11;
int echoPin1 = 12;
int echoPin2 = 13;
int enL = 9;
int enR = 10;
// defines variables
int duration1;
int duration2;
int distance1;
int distance2;
int cdistance1;
int cdistance2;
void setup() {
Serial.begin(9600);
pinMode(trigPin1, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin1, INPUT); // Sets the echoPin as an 
pinMode(trigPin2, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin2, INPUT); // Sets the echoPin as an Input
pinMode(Lmotorpin1, OUTPUT);
pinMode(Lmotorpin2, OUTPUT);
pinMode(Rmotorpin1, OUTPUT);
pinMode(Lmotorpin2, OUTPUT);
pinMode(enL, OUTPUT);
pinMode(enR, OUTPUT);
}
/*Needs to be looped*/
void loop(){
// Clears the trigPin
digitalWrite(trigPin1, LOW);
delayMicroseconds(2000);
// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin1, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin1, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration1= pulseIn(echoPin1, HIGH);
delay(500);
digitalWrite(trigPin2, LOW);
delayMicroseconds(2000);
// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin2, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin2, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration2= pulseIn(echoPin2, HIGH);
// Calculating the distance in cm
distance1= duration1*0.034/2;
distance2= duration2*0.034/2;
cdistance1=distance1+5;
cdistance2=distance2+5;
Serial.println(distance1);
Serial.println(distance2);
if (distance1 > distance2) {
  digitalWrite(Lmotorpin1,LOW);
  digitalWrite(Lmotorpin2,HIGH);
  digitalWrite(Rmotorpin1,HIGH);
  digitalWrite(Rmotorpin2,LOW);
  analogWrite(enL,1000);
  analogWrite(enR,1000);
  Serial.println("R");
  delay(1000);
  digitalWrite(Lmotorpin1,LOW);
  digitalWrite(Lmotorpin2,LOW);
  digitalWrite(Rmotorpin1,LOW);
  digitalWrite(Rmotorpin2,LOW);
}
else if (distance1 < distance2) {
  digitalWrite(Lmotorpin1,HIGH);
  digitalWrite(Lmotorpin2,LOW);
  digitalWrite(Rmotorpin1,LOW);
  digitalWrite(Rmotorpin2,HIGH);
  analogWrite(enL,1000);
  analogWrite(enR,1000);
  Serial.println("L");
  delay(1000);
  digitalWrite(Lmotorpin1,LOW);
  digitalWrite(Lmotorpin2,LOW);
  digitalWrite(Rmotorpin1,LOW);
  digitalWrite(Rmotorpin2,LOW);
}
else {
  Serial.println("Done");
  delay(1000);
}
}

/*int finddistance(){
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2000);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration1= pulseIn(echoPin1, HIGH);
  distance1= duration1*0.034/2;
  return distance1;
}*/

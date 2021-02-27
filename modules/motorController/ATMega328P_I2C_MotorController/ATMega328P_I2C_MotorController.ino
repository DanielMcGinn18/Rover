/*
  Arduino Slave for Raspberry Pi Master
  Connects to Raspberry Pi via I2C
*/

// Include the Wire library for I2C
#include <Wire.h>
 
// LED on pin 13
const int ledPin = 13; 

//motor A connected between A01 and A02

int STBY = 4; //standby
int x, Motor, Direction, Speed; // initilize variable

//Motor A
int PWMA = 5; //Speed control
int AIN2 = 2; //Direction
int AIN1 = 6; //Direction
 
void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);

  // Setup Serial Monitor
  Serial.begin(9600);

pinMode(STBY, OUTPUT);
pinMode(PWMA, OUTPUT);
pinMode(AIN1, OUTPUT);
pinMode(AIN2, OUTPUT);

  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  
  // Setup pin 13 as output and turn LED off
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}
 
// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    digitalWrite(ledPin, c);
    Direction = 1; // Forward
    Speed = c*2; // Speed
    Motor = 1;
  
  if(Speed > 0){
  move(Motor, Speed, Direction); //motor 1
  }else{
  stop();
  }
  }
}
void loop() {
  delay(200);
}

void move(int motor, int motorSpeed, int motorDirection){
//speed: 0 is off, and 255 is full speed
//direction: 0 clockwise, 1 counter-clockwise
  Serial.print("motor:");
  Serial.print(motor);
  Serial.print("     motorSpeed:");
  Serial.print(motorSpeed);
  Serial.print("     motorDirection:");
  Serial.println(motorDirection);

digitalWrite(STBY, HIGH); //disable standby

boolean inPin1 = LOW;
boolean inPin2 = HIGH;

if(motorDirection == 1){
inPin1 = HIGH;
inPin2 = LOW;
}

if(motor == 1){
digitalWrite(AIN1, inPin1);
digitalWrite(AIN2, inPin2);
analogWrite(PWMA, motorSpeed);
}
}

void stop(){
//enable standby
digitalWrite(STBY, LOW);
}

/*
  Arduino Slave for Raspberry Pi Master
  Connects to Raspberry Pi via I2C
*/

// Include the Wire library for I2C
#include <Wire.h>
 
#define LED_PIN 13
boolean ledon = HIGH;
// initialize the library with the numbers of the interface pins

byte slave_address = 7;

//motor A connected between A01 and A02
//motor B connected between B01 and B02

int STBY = 4; //standby
int x, motorA, directionA, speedA, motorB, directionB, speedB; // initilize variable

//Motor A
int PWMA = 5; //Speed control
int AIN2 = 2; //Direction
int AIN1 = 6; //Direction

//Motor B
int PWMB = 9; //Speed control
int BIN1 = 7; //Direction
int BIN2 = 8; //Direction
 
void setup() {
  pinMode(STBY, OUTPUT);
  
  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);

  pinMode(PWMB, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  
  Wire.begin(slave_address);
  Wire.onReceive(receiveEvent);
  
  Serial.begin(9600); // Setup Serial Monitor
}
 
void loop() {

}

void receiveEvent(int howMany) {
  int numOfBytes = Wire.available();
  //display number of bytes and cmd received, as bytes
  Serial.print("numOfBytes:");
  Serial.println(numOfBytes);

  int dataArray[numOfBytes];

  byte b = Wire.read();  //cmd
  Serial.print("cmd:");
  Serial.println(b);


  //display message received, as char
  for(int i=0; i<numOfBytes-1; i++){
    char data = Wire.read();
    dataArray[i] = int(data);
    Serial.print("data:");
    Serial.println(int(data));
  }
  motorA = dataArray[0];
  directionA = dataArray[1];
  speedA = dataArray[2]*2;

  motorB = dataArray[3];
  directionB = dataArray[4];
  speedB = dataArray[5]*2;

  if (speedA > 0 || speedB > 0) {
  move(motorA, speedA, directionA); //motor A
  move(motorB, speedB, directionB); //motor B
  }else{
  stop();
  }
  toggleLED();
}

void toggleLED(){
  ledon = !ledon;
  if(ledon){
    digitalWrite(LED_PIN, HIGH);
  }else{
    digitalWrite(LED_PIN, LOW);
  }
}


void move(int motor, int motorSpeed, int motorDirection){
//speed: 0 is off, and 255 is full speed
//direction: 0 backward, 1 forward
  Serial.print("motor:");
  Serial.print(motor);
  Serial.print("     motorDirection:");
  Serial.print(motorDirection);
  Serial.print("     motorSpeed:");
  Serial.println(motorSpeed);

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
}else{
digitalWrite(BIN1, inPin1);
digitalWrite(BIN2, inPin2);
analogWrite(PWMB, motorSpeed);
}
}

void stop(){
//enable standby
digitalWrite(STBY, LOW);
Serial.println("STOP");
}

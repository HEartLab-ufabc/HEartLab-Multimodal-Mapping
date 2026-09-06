#include <AccelStepper.h>

// Define stepper motor connections and motor interface type.
#define motorInterfaceType 1
#define dirPin 5
#define stepPin 2

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

const int microStep = 16;
const float stepsPerRevolution = microStep*200;
const float stepsPerDegree = stepsPerRevolution/360;
int incomingInt = 0;  // initiation variable
float incomingAngle = 0; // Angle to move to

int stepCount = 0;         // number of steps the motor will take
int moveFor = 0;

void setup() {
  // initialize the serial port:
  Serial.begin(57600);
  pinMode(stepPin,OUTPUT);
  pinMode(dirPin,OUTPUT);

  stepper.setMaxSpeed(400); // Maximun speed of the motor
  stepper.setAcceleration(100); // Acceleration of the motor
}

void loop() {
  if (Serial.available() > 1) {    
    incomingInt = recvData();
    Serial.print("incomingInt: ");
    Serial.println(incomingInt);
    
    incomingAngle = recvData();
    Serial.print("incomingAngle: ");
    Serial.println(incomingAngle);    

    // Move to: Angle
    moveFor = stepsPerDegree*incomingAngle;
    stepCount = stepCount + moveFor;
    
    stepper.moveTo(stepCount);   
    stepper.runToPosition();
      
    // say how many steps you run:
    Serial.print("Step Count: ");
    Serial.println(stepCount);
    Serial.flush();
    }
  }


// Receive data from Serial
float recvData(){
  digitalWrite(13,LOW);
  delay(1);
  digitalWrite(13,HIGH);
  float incomingData = Serial.parseFloat();
 
  return incomingData;
}

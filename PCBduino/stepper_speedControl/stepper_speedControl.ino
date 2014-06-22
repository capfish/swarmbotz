
#include <Stepper.h>


const int stepsPerRevolution = 24; 

//Stepper leftStepper(stepsPerRevolution, 7,A1,8,A0);           
//Stepper rightStepper(stepsPerRevolution, 3,6,4,5);
//Stepper leftStepper(stepsPerRevolution, 7,A1,8,A0); 
Stepper rightStepper(stepsPerRevolution, 3,4,5,6);

int led = A3;
boolean ledState = LOW;
long leftVelocity = 0;
long rightVelocity = 0;


void setup() {
leftVelocity = 50;
rightVelocity = 50; 
}

void loop() {
    //positive values go backwards on the left motor, forwards on the right motor

    leftStepper.setSpeed(abs(leftVelocity));
    rightStepper.setSpeed(abs(rightVelocity));

    if (leftVelocity>0){
      leftStepper.step(-stepsPerRevolution/10);
    }
    else {
      leftStepper.step(stepsPerRevolution/10);
    }
    
    if (rightVelocity>0){
      rightStepper.step(stepsPerRevolution/10);
    }
    else {
      rightStepper.step(-stepsPerRevolution/10);
    }
}


void blink() {
  if (ledState == HIGH) {
    ledState = LOW;
    digitalWrite(led, ledState);
    delay(100);
  }
  else {
    ledState = HIGH;
    digitalWrite(led, ledState);
    delay(100);
  }
}



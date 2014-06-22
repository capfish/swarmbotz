
/* 
 Stepper Motor Control - one step at a time
 
 This program drives a unipolar or bipolar stepper motor. 
 The motor is attached to digital pins 8 - 11 of the Arduino.
 
 The motor will step one step at a time, very slowly.  You can use this to
 test that you've got the four wires of your stepper wired to the correct
 pins. If wired correctly, all steps should be in the same direction.
 
 Use this also to count the number of steps per revolution of your motor,
 if you don't know it.  Then plug that number into the oneRevolution
 example to see if you got it right.
 
 Created 30 Nov. 2009
 by Tom Igoe
 
 */

#include <Stepper.h>

const int stepsPerRevolution = 24;  // change this to fit the number of steps per revolution
                                     // for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 7,A1,8,A0);            
Stepper myStepper2(stepsPerRevolution, 3,6,4,5);   //U2, near the ICSP header

int stepCount = 0;         // number of steps the motor has taken
int led = A4;
boolean ledState = LOW;

void setup() {
  // initialize the serial port:
  Serial.begin(9600);
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
    pinMode(A4, OUTPUT);
}

void loop() {
  // step one step:
  myStepper.step(1);
  myStepper2.step(1);
  Serial.print("steps:" );
  Serial.println(stepCount);
  stepCount++;
      blink();

  delay(500);
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
    delay(10);
  }
}


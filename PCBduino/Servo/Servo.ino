// Controlling a servo position using a potentiometer (variable resistor) 
// by Michal Rinott <http://people.interaction-ivrea.it/m.rinott> 

#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
Servo myservo2;  // create servo object to control a servo 
 

void setup() 
{ 
  myservo.attach(3);  // attaches the servo on pin 9 to the servo object 
  myservo2.attach(4);  // attaches the servo on pin 9 to the servo object 

} 
 
void loop() 
{ 
  myservo.write(120);                  // sets the servo position according to the scaled value 
  myservo2.write(80);                  // sets the servo position according to the scaled value 
  delay(500);                           // waits for the servo to get there 
  myservo.write(60);
  myservo2.write(140);
  delay(500);
} 

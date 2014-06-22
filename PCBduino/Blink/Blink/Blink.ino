// FAT SIDE IS GND
// 1 for PCBduino red led, A2 is IR, A3 red, A4 green, A5 blue 
int led = 1;
int led2 = A2;
int led3 = A3;
int led4 = A4;
int led5 = 2;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);     
  pinMode(led2, OUTPUT);     
  pinMode(led3, OUTPUT);     
  pinMode(led4, OUTPUT);     
  pinMode(led5, OUTPUT);     

}

// the loop routine runs over and over again forever:
void loop() {
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(led5, HIGH);   // turn the LED on (HIGH is the voltage level)

  digitalWrite(led2, LOW);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(led3, LOW);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(led4, LOW);   // turn the LED on (HIGH is the voltage level)
  delay(200);               // wait for a second
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(led5, LOW);   // turn the LED on (HIGH is the voltage level)
  
  digitalWrite(led2, HIGH);    // turn the LED off by making the voltage LOW
  digitalWrite(led3, HIGH);    // turn the LED off by making the voltage LOW
  digitalWrite(led4, HIGH);    // turn the LED off by making the voltage LOW
  delay(200);               // wait for a second
}


// Reset button test
//void loop() {
//  for (int i=100; i<1000; i +=100){
//  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delay(i);               // wait for a second
//  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
//  delay(i);               // wait for a second
//  }
//}


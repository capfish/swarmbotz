// https://gist.github.com/jamesotron/766994
// works with common anode LEDs
// http://www.optekinc.com/datasheets/OVSARGB4R8.pdf, with 1k series resistors to limit current
// put a piece of paper over the LED to limit retina damage
// remember to use PWM-capable pins for analogWrite!

const int redPin = 3;
const int greenPin = 5;
const int bluePin = 6;
 
void setup() {
// Start off with the LED off.
setColourRgb(0,0,0);
}
 
void loop() {
unsigned int rgbColour[3];
 
// Start off with red.
rgbColour[0] = 255;
rgbColour[1] = 0;
rgbColour[2] = 0;
 
// Choose the colours to increment and decrement.
for (int decColour = 0; decColour < 3; decColour += 1) {
int incColour = decColour == 2 ? 0 : decColour + 1;
 
// cross-fade the two colours.
for(int i = 0; i < 255; i += 1) {
rgbColour[decColour] -= 1;
rgbColour[incColour] += 1;
setColourRgb(rgbColour[0], rgbColour[1], rgbColour[2]);
delay(5);
}
}
}
 
void setColourRgb(unsigned int red, unsigned int green, unsigned int blue) {
analogWrite(redPin, red);
analogWrite(greenPin, green);
analogWrite(bluePin, blue);
}

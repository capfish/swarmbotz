    /*
    Adafruit Arduino - Lesson 3. RGB LED
    */
    // https://learn.adafruit.com/adafruit-arduino-lesson-3-rgb-leds/arduino-sketch
    // use PWM pins!
    
    int redPin = 3;
    int greenPin = 5;
    int bluePin = 6;
     
    //uncomment this line if using a Common Anode LED
    #define COMMON_ANODE
     
    void setup()
    {
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
    }
     
    void loop()
    {
    setColor(255, 0, 0); // red
    delay(1000);
    setColor(0, 255, 0); // green
    delay(1000);
    setColor(0, 0, 255); // blue
    delay(2000);
    setColor(255, 255, 0); // yellow
    delay(1000);
    setColor(80, 0, 80); // purple
    delay(1000);
    setColor(0, 255, 255); // aqua
    delay(2000);
    }
     
    void setColor(int red, int green, int blue)
    {
    #ifdef COMMON_ANODE
    red = 255 - red;
    green = 255 - green;
    blue = 255 - blue;
    #endif
    analogWrite(redPin, red);
    analogWrite(greenPin, green);
    analogWrite(bluePin, blue);
    }

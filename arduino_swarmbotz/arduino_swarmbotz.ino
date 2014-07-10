/*********************************************************************
This is an example for our nRF8001 Bluetooth Low Energy Breakout

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/1697

Adafruit invests time and resources providing this open source code, 
please support Adafruit and open-source hardware by purchasing 
products from Adafruit!

Written by Kevin Townsend/KTOWN  for Adafruit Industries.
MIT license, check LICENSE for more information
All text above, and the splash screen below must be included in any redistribution
*********************************************************************/

// This version uses call-backs on the event and RX so there's no data handling in the main loop!

#include <SPI.h>
#include <Servo.h> 
#include "Adafruit_BLE_UART.h"

#define ADAFRUITBLE_REQ A1
#define ADAFRUITBLE_RDY 2
#define ADAFRUITBLE_RST A0

Adafruit_BLE_UART uart = Adafruit_BLE_UART(ADAFRUITBLE_REQ, ADAFRUITBLE_RDY, ADAFRUITBLE_RST);

int absSpeed = 90;
int fSpeed = 90;
int bSpeed = 90;
//int pktNumber = 0;

Servo Lservo;  // create servo object to control a servo 
Servo Rservo;  // create servo object to control a servo 

int redPin = 3;
int greenPin = 5;
int bluePin = 6;
#define COMMON_ANODE
// #define DEBUG
    
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

/**************************************************************************/
/*!
    This function is called whenever select ACI events happen
*/
/**************************************************************************/
void aciCallback(aci_evt_opcode_t event)
{
  switch(event)
  {
    case ACI_EVT_DEVICE_STARTED:
      Serial.println(F("Advertising started"));
      break;
    case ACI_EVT_CONNECTED:
      Serial.println(F("Connected!"));
      break;
    case ACI_EVT_DISCONNECTED:
      Serial.println(F("Disconnected or advertising timed out"));
      break;
    default:
      break;
  }
}

/**************************************************************************/
/*!
    This function is called whenever data arrives on the RX channel
*/
/**************************************************************************/
void rxCallback(uint8_t *buffer, uint8_t len)
{
  #ifdef DEBUG
  Serial.print(F("Received "));
  Serial.print(len);
  Serial.print(F(" bytes: "));
 
//  else: do nothing

  for(int i=0; i<len; i++){
    byte msg = (byte)buffer[i];
    Serial.print(msg); 
  }

  Serial.print(F(" ["));

  for(int i=0; i<len; i++)
  {
    Serial.print(" 0x"); Serial.print((byte)buffer[i], HEX); 
//    Serial.print(" 0b"); Serial.print((byte)buffer[i], BIN); 
//    Serial.print(" "); Serial.print((byte)buffer[i], DEC);
  }
  Serial.println(F(" ]"));
  //Serial.println('cmd received: '); Serial.print(buffer[0]); Serial.print(buffer[1]); Serial.println(buffer[2]);

  #endif
  
  if ((byte)buffer[0] == (byte)10){ //color cmd received
    setColor(buffer[1],buffer[2], buffer[3]);
  }
  else if ((byte)buffer[0] == (byte)20){ //string cmd received
    Lservo.write(buffer[1]);
    Rservo.write(map(buffer[2],0,180,180,0));
  }
  

//  Serial.print("Packet number: ");Serial.println(pktNumber);
//  pktNumber++;

  /* Echo the same data back! */
  //uart.write(buffer, len);
}

/**************************************************************************/
/*!
    Configure the Arduino and start advertising with the radio
*/
/**************************************************************************/
void setup(void)
{ 
  #ifdef DEBUG
  Serial.begin(115200);
  while(!Serial); // Leonardo/Micro should wait for serial init
  Serial.println(F("Adafruit Bluefruit Low Energy nRF8001 Callback Echo demo"));
  #endif
  
  uart.setRXcallback(rxCallback);
  uart.setACIcallback(aciCallback);
  uart.begin();
  
  Lservo.attach(7); // this way stops at 90
  Rservo.attach(8); 
  Lservo.write(90);
  Rservo.write(90);
  
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
  setColor(255,255,255);
  delay(100);
  setColor(0,0,0);

}

/**************************************************************************/
/*!
    Constantly checks for new events on the nRF8001
*/
/**************************************************************************/
void loop()
{
  uart.pollACI();
}

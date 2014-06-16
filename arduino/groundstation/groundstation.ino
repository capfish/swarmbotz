#include <SPI.h>

// NRF Register addresses
const byte CONFIG = 0x00;
const byte EN_AA = 0x01;
const byte EN_RXADDR = 0x02;
const byte SETUP_AW = 0x03;
const byte SETUP_RETR = 0x04;
const byte RF_CH = 0x05;
const byte RF_SETUP = 0x06;
const byte STATUS = 0x07;
const byte RX_ADDR_P0 = 0x0A;
const byte TX_ADDR = 0x10;
const byte RX_PW_P0 = 0x11;
const byte FIFO_STATUS = 0x17;
// Values to write to registers
const byte TXMODE = 0x3A;        //only RX_DR enabled, PWR_UP 1, PRIM_RX 0, CRC 1
const byte RXMODE = 0x3B;       //only RX_DR enabled, PWR_UP 1, PRIM_RX 1, CRC 1
const byte CLRIRQ = 0x7E;       //writes 1 to FIFO_STATUS to clear interrupt
const byte EN_DP0 = 0x01;       //enables only data pipe 0
const byte AW_3B = 0x01;        //address width for 3bytes
const byte FREQ = 0x44;         //frequency to 2.444 GHz
const byte DR_PWR = 0x0E;       //sets data rate and power
const byte PW = 0x01;           //payload width
const byte ADDR1B = 0x22;       //the three address bytes
const byte ADDR2B = 0x22;
const byte ADDR3B = 0x22;
// nRF commands
const byte R_RX_PAYLOAD = 0x61;
const byte W_TX_PAYLOAD = 0xA0;
const byte FLUSH_TX = 0xE1;
const byte FLUSH_RX = 0xE2;
//nRF pin assignments
const int nRF = 9;          //p3.5
const int nRFCSN = 10;
const int IRQ = 2;

void setup() {
  pinMode(nRF, OUTPUT);
  pinMode(nRFCSN, OUTPUT);
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);
  SPI.setDataMode(SPI_MODE0);
  digitalWrite(nRFCSN, HIGH);
  Serial.begin(9600);
  setupnRF();
}
void loop() {
  if(Serial.available() > 0) {
    byte input[1];
    input[0] = Serial.read();
    transmitPacket(input, sizeof(input));
    Serial.println(input[0]);
  }
}

void transmitPacket(byte data[], size_t datalength) {
  digitalWrite(nRF, LOW);
  nRFWriteRegister(CONFIG,TXMODE);
  nRFWriteCommand(FLUSH_TX);
  digitalWrite(nRFCSN, LOW);
  delayMicroseconds(1);
  SPI.transfer(W_TX_PAYLOAD);
  for(byte i = 0; i < datalength; i++) {
    SPI.transfer(data[i]);
  }
  digitalWrite(nRFCSN,HIGH);
  delayMicroseconds(1);
  digitalWrite(nRF, HIGH);
  delayMicroseconds(50);
  digitalWrite(nRF, LOW);
}  

void nRFWriteRegister(byte reg, byte value) {
  digitalWrite(nRFCSN, LOW);
  delayMicroseconds(1);
  reg += 0x20;  //change to write command
  SPI.transfer(reg);
  SPI.transfer(value);
  digitalWrite(nRFCSN, HIGH);
  delayMicroseconds(1);
}

void nRFWriteAddress(byte reg, byte addr1, byte addr2, byte addr3) {
  digitalWrite(nRFCSN, LOW);
  delayMicroseconds(1);
  reg += 0x20;
  SPI.transfer(reg);
  SPI.transfer(addr1);
  SPI.transfer(addr2);
  SPI.transfer(addr3);
  digitalWrite(nRFCSN, HIGH);
  delayMicroseconds(1);
}

void nRFWriteCommand(byte command){
  digitalWrite(nRFCSN, LOW);
  delayMicroseconds(1);
  SPI.transfer(command);
  digitalWrite(nRFCSN, HIGH);
  delayMicroseconds(1);
}

void setupnRF() {
  digitalWrite(nRF, LOW);
  nRFWriteRegister(CONFIG, 0); //reset CONFIG
  nRFWriteRegister(EN_AA,0); //disable auto-acknowledge
  nRFWriteRegister(EN_RXADDR, EN_DP0); //enable only data pipe 0
  nRFWriteRegister(SETUP_AW, AW_3B); //set address width to 3 bytes
  nRFWriteRegister(SETUP_RETR, 0); //disable auto retransmit
  nRFWriteRegister(RF_CH, FREQ); //change frequency to 2.444GHz
  nRFWriteRegister(RF_SETUP, DR_PWR); //1 MBps data rate -12dBm power
  nRFWriteRegister(RX_PW_P0, PW); //Set payload width for DP0
  nRFWriteAddress(RX_ADDR_P0, ADDR1B, ADDR2B, ADDR3B); //setup RX address to be whatever is in ADDR*B
  nRFWriteAddress(TX_ADDR, ADDR1B, ADDR2B, ADDR3B); //same address for TX
  nRFWriteRegister(CONFIG, TXMODE);
  delayMicroseconds(150);
  nRFWriteCommand(FLUSH_TX);
  nRFWriteRegister(CONFIG, RXMODE); //put the nRF in RX and mask all but RX_DR
  nRFWriteCommand(FLUSH_RX); //get rid of anything left in the RX FIFO
  digitalWrite(nRF, HIGH); //enable the chip to go into RX
  delayMicroseconds(150);
}

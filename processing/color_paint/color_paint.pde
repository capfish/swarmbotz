import processing.serial.*; //This allows us to use serial objects
import processing.net.*; // Use server objects

Server serve;
int serverPort = 4000;
 
Serial port; // Create object from Serial class
Coordinate point = new Coordinate();
float[] lastDrawnPoint = {0.0,0.0};
int width = 640;
int height = 480;
int colorBar = 60;
int boxSize = 40;
int numColors = 6;
String dataPacket;
color[] boxColors = {#FF0000, #00FF00, #0000FF, #FFFF00, #00FFFF, #FF00FF};

void setup() {
  size(width, height + colorBar);
  noSmooth();
  
  background(102);
  fill(#FFFFFF);
  rect(0, 480, 640, 5);
  
  fill(255,0,0); // Red rectangle
  rect(10, 490, boxSize, boxSize);
  fill(0,255,0); // Green rectangle
  rect(60, 490, boxSize, boxSize);
  fill(0,0,255); // Blue rectangle
  rect(110, 490, boxSize, boxSize);
  fill(255,255,0); // Yellow rectangle
  rect(160, 490, boxSize, boxSize);
  fill(0,255,255);  // Cyan rectangle
  rect(210, 490, boxSize, boxSize);
  fill(255,0,255); // Magenta rectangle
  rect(260, 490, boxSize, boxSize);
  fill(255,255,255); // Magenta rectangle
  rect(590, 490, boxSize, boxSize);
  fill(126);
  //  println(Serial.list()); //This shows the various serial port option0
  //String portName = Serial.list()[0]; //The serial port should match the one the Arduino is hooked to
  //port = new Serial(this, portName, 9600); //Establish the connection rate
  dataPacket = "No data";
  serve = new Server(this, serverPort);

}

void draw() {

  serve.write(dataPacket);
  println("No data");
}

/* mousePressed() keeps track of mouse clicks
   and sends the coordinates over serial */
void mousePressed() {
  
  stroke(0, 255, 0);
  
  if(inbounds(mouseX, mouseY)) {
      ellipse(mouseX,mouseY,10,10);
      point.mapCoordinates(mouseX, mouseY, width, height); //get adjusted coordinates
      //println(str(mouseX) + ',' + str(mouseY));
      point.getAngles(point.x, point.y); //change coordinates to angles
      point.angles2String(point.theta1, point.theta2); //prepare angles for serail
      //port.write(point.serialLine); //send the angles over serial
      //print(point.serialLine);
      lastDrawnPoint[0] = mouseX;
      lastDrawnPoint[1] = mouseY;
      String coordinates = str(mouseX) + ',' + str(mouseY);
      //println(coordinates);
      dataPacket = coordinates;
      //dataPacket = coordinates;
      //serve.write(coordinates);
  }
  else {
    for (int i = 0; i < numColors; i++) {
      if (overBox(mouseX, mouseY, 10 + i*(boxSize + 10), 490)){
        fill(boxColors[i]);
        stroke(boxColors[i]);
        rect(0, 480, 640, 5);
        dataPacket = "c:" + str(boxColors[i]);
      }
    }
    if (overBox(mouseX, mouseY, 590, 490)) {
      fill(#FFFFFF);
      stroke(#FFFFFF);
      rect(0, 480, 640, 5);
      dataPacket = "c:" + color(#000000);
    }    
  }
  fill(126);
}


void mouseReleased() {
  
  stroke(0, 0, 255);
  
  if(inbounds(mouseX, mouseY)) {
      ellipse(mouseX,mouseY,10,10);
      point.mapCoordinates(mouseX, mouseY, width, height); //get adjusted coordinates
      println(str(mouseX) + ',' + str(mouseY));
      point.getAngles(point.x, point.y); //change coordinates to angles
      point.angles2String(point.theta1, point.theta2); //prepare angles for serail
      //port.write(point.serialLine); //send the angles over serial
      //print(point.serialLine);
      lastDrawnPoint[0] = mouseX;
      lastDrawnPoint[1] = mouseY;
      //serve.write(dataPacket);
      println(dataPacket);
  }
}

/* mouseDragged() keeps track of the mouse
   coordinates while being dragged and sends
   them over serial*/
void mouseDragged() {
  
  if(inbounds(mouseX, mouseY)) {
      point.mapCoordinates(mouseX, mouseY, width, height); //get adjusted coordinates
      point.getAngles(point.x, point.y); //change coordinates to angles
      point.angles2String(point.theta1, point.theta2); //prepare them for serial
      //port.write(point.serialLine); //send them over serial
      //println(point.serialLine + " " + dist(point.x, point.y, lastDrawnPoint.x, lastDrawnPoint.y)+ " ");
      //println(point.x);
      if (dist(mouseX, mouseY, lastDrawnPoint[0], lastDrawnPoint[1]) > 50) {
        stroke(255, 0, 0);
        ellipse(mouseX,mouseY,10,10);
        lastDrawnPoint[0] = mouseX;
        lastDrawnPoint[1] = mouseY;
        dataPacket += ':' + str(mouseX) + ',' + str(mouseY);
        print("Draw green");
        
      }
      else {
        stroke(255);
        ellipse(mouseX,mouseY,5,5);
      }
  }
  
}

void keyPressed() {
    if(key == 'r') {
        background(102);
        fill(#FFFFFF);
        rect(0, 480, 640, 5);
  
        fill(255,0,0); // Red rectangle
        rect(10, 490, boxSize, boxSize);
        fill(0,255,0); // Green rectangle
        rect(60, 490, boxSize, boxSize);
        fill(0,0,255); // Blue rectangle
        rect(110, 490, boxSize, boxSize);
        fill(255,255,0); // Yellow rectangle
        rect(160, 490, boxSize, boxSize);
        fill(0,255,255);  // Cyan rectangle
        rect(210, 490, boxSize, boxSize);
        fill(255,0,255); // Magenta rectangle
        rect(260, 490, boxSize, boxSize);
        fill(255,255,255); // Magenta rectangle
        rect(590, 490, boxSize, boxSize);
        fill(126);
    }
}

/* inbounds() checks to see if the mouse position
   is actually on the drawing window */
boolean inbounds(int x, int y) {
    if(x > 0 && y > 0 && x < width && y < height){
        return true;
    } else {
        return false;
    }
}

/* Checks to see whether the mouse is over a color box.
(x, y) = mouse pos
(xBox, yBox) = top left corner of box */
boolean overBox(int x, int y, int xBox, int yBox) {
  if(x > xBox && x < xBox + boxSize && y > yBox && y < yBox + boxSize) {
    return true; }
  else {
    return false; }
}



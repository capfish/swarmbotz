import processing.serial.*; //This allows us to use serial objects
import processing.net.*; // Use server objects

Server serve;
int serverPort = 4000;
 
Serial port; // Create object from Serial class
Coordinate point = new Coordinate();
float[] lastDrawnPoint = {0.0,0.0};
int width = 640;
int height = 480;
String dataPacket;

void setup() {
  size(width, height);
  noSmooth();
  fill(126);
  background(102);
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
  ellipse(mouseX,mouseY,10,10);
  if(inbounds(mouseX, mouseY)) {
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
      //serve.write(coordinates);
  }
}

void mouseReleased() {
  
  stroke(0, 0, 255);
  ellipse(mouseX,mouseY,5,5);
  if(inbounds(mouseX, mouseY)) {
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

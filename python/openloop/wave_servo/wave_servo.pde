int rad = 60; 
float x1pos, x2pos, x3pos, y1pos, y2pos, y3pos; 

float y1speed = -8.0;
float y2speed = -8.0;
float y3speed = -8.0;
float y1delta = 0.25;
float y2delta = 0.25;
float y3delta = 0.25;

int count = 0;

PShape dot;

import processing.net.*;
Client myClient;
PrintWriter output;


void setup()
{
 //myClient = new Client(this, "127.0.0.1", 5207);
 output = createWriter("positions.txt"); 


  size(640, 640);
  noStroke();
  frameRate(30);
  ellipseMode(RADIUS);
  x1pos = width/4;
  x2pos = width/2;
  x3pos = (3*width)/4;

  y1pos = height/2;
  y2pos = height/2;
  y3pos = height/2;
  
  dot = loadShape("circle-arrow-up.svg");
}

void draw()
{
  background(255,255,255);
  count = count +1; 

  if (y1pos >0 && y1pos <= height/2)
  {
    y1speed = y1speed +(y1delta);
    y1pos = y1pos + y1speed;
  }
  
  if (count > 10)
  {
    if (y2pos >0 && y2pos <=height/2)
    {
      y2speed = y2speed +(y2delta);
      y2pos = y2pos + y2speed;
    }
  }

  if (count > 20)
  {
    if (y3pos >0 && y3pos <=height/2)
    {
      y3speed = y3speed +(y3delta);
      y3pos = y3pos + y3speed;
    }
  }

  shape(dot,x1pos, y1pos, rad, rad);
  shape(dot,x2pos, y2pos, rad, rad);
  shape(dot,x3pos, y3pos, rad, rad);
//  output.println("0,"+int(x1pos) +","+ int(y1pos));
//  output.println("1,"+int(x2pos) +","+ int(y2pos));
//  output.println("2,"+int(x3pos) +","+ int(y3pos));
//  
//  
  

  if (count > 90){
//    output.flush(); // Writes the remaining data to the file
//    output.close(); // Finishes the file
    exit();
  }

}

void formatCmd(int botid, int cmd){
}

void driveServos(Client client, int botid, boolean reverseFlag, int dx, int dy, float dtheta){
}

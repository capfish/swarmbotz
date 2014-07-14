import processing.net.*; 

Client myClient;

int boxSize = 50;
int buttonSizeX = 20;
int buttonSizeY= 10;
boolean overBoxUp = false;
boolean overBoxDown = false;
boolean overBoxLeft = false;
boolean overBoxRight = false;
boolean overButton1 = false;
boolean overButton2 = false;
boolean overButton3 = false;
boolean Uplocked = false;
boolean Downlocked = false;
boolean Rightlocked = false;
boolean Leftlocked = false;
boolean robot1 = false;
boolean robot2 = false;
boolean robot3 = false;

float upx, upy, downx, downy, leftx, lefty, rightx, righty, button1x, button2x, button3x, buttony;
PShape up, down, left, right;

String[] outputs = new String[3];

void setup() 
{
  size(500, 600);
  upx = width/2.0;
  upy = (2*height)/5.0;
  downx = width/2.0;
  downy = (4*height)/5.0;
  leftx = width/5.0;
  lefty = (3*height)/5.0;
  rightx = (4*width)/5.0;
  righty = (3*height)/5.0;
  button1x=width/5.0;
  buttony=height/7.0;
  button2x=(2.5*width)/5.0;
  button3x=(4*width)/5.0;

  rectMode(RADIUS);  

  up = loadShape("up.svg");
  down = loadShape("down.svg");
  left = loadShape("turn_left.svg");
  right = loadShape("turn_right.svg");
  
  myClient = new Client(this, "127.0.0.1", 5207);
}

void draw() 
{ 
  background(255);

  // Test if the cursor is over the box 
  if (mouseX > upx-boxSize && mouseX < upx+boxSize && mouseY > upy-boxSize && mouseY < upy+boxSize) 
    overBoxUp = true;  
  else if (mouseX > downx-boxSize && mouseX < downx+boxSize && mouseY > downy-boxSize && mouseY < downy+boxSize)
    overBoxDown = true;
  else if (mouseX > rightx-boxSize && mouseX < rightx+boxSize && mouseY > righty-boxSize && mouseY < righty+boxSize)
    overBoxRight = true;
  else if (mouseX > leftx-boxSize && mouseX < leftx+boxSize && mouseY > lefty-boxSize && mouseY < lefty+boxSize)
    overBoxLeft = true;
  else if (mouseX > button1x- buttonSizeX && mouseX < button1x+buttonSizeX && mouseY > buttony-buttonSizeY && mouseY < buttony+buttonSizeY)
    overButton1 = true;
  else if (mouseX > button2x- buttonSizeX && mouseX < button2x+buttonSizeX && mouseY > buttony-buttonSizeY && mouseY < buttony+buttonSizeY)
    overButton2 = true;
  else if (mouseX > button3x- buttonSizeX && mouseX < button3x+buttonSizeX && mouseY > buttony-buttonSizeY && mouseY < buttony+buttonSizeY)
    overButton3 = true;
  else 
  {
    stroke(153);
    fill(153);
    overBoxUp = false;
    overBoxLeft = false;
    overBoxRight = false;
    overBoxDown = false;
    overButton1 = false;
    overButton2 = false;
    overButton3 = false;
  }

  // Draw the box
  if(Uplocked == false)
  {
  fill(153);
  rect(upx, upy, boxSize, boxSize);
  }
  else if(Uplocked == true)
  {
    stroke(0);
    fill(255);
    rect(upx, upy, boxSize, boxSize);
  }
  if(Downlocked == false)
  {
    fill(153);
    rect(downx, downy, boxSize, boxSize);
  }
  else if(Downlocked == true)
  {
    stroke(0);
    fill(255);
    rect(downx, downy, boxSize, boxSize);
  }
  if(Leftlocked == false)
  {
    fill(153);
    rect(leftx, lefty, boxSize, boxSize);
  }
  else if(Leftlocked == true)
  {
    stroke(0);
    fill(255);
    rect(leftx, lefty, boxSize, boxSize);
  }
  if(Rightlocked == false)
  {
    fill(153);
    rect(rightx, righty, boxSize, boxSize);
  }
  else if(Rightlocked == true)
  {
    stroke(0);
    fill(255);
    rect(rightx, righty, boxSize, boxSize);
  }

  fill(153);
  textSize(30);
  text("ROBOT 1", width/11.0, height/9.0);
  text("ROBOT 2", (4.3*width)/11.0, height/9.0);
  text("ROBOT 3", (7.5*width)/11.0, height/9.0);
  shape(up, upx, upy, boxSize, boxSize);
  shape(down, downx, downy, boxSize, boxSize);
  shape(left, leftx, lefty, boxSize, boxSize);
  shape(right, rightx, righty, boxSize, boxSize);
  
  if (robot1 == false)
  {
    fill(255, 0, 0);
    rect(button1x, buttony, buttonSizeX, buttonSizeY);
    fill(0);
    textSize(20);
    text("OFF", width/6.0, height/6.4);
  } else if (robot1 == true)
  {
    fill(0, 255, 0);
    rect(button1x, buttony, buttonSizeX, buttonSizeY);
    fill(0);
    textSize(20);
    text("ON", width/5.8, height/6.4);
  }
  if (robot2== false)
  {
    fill(255, 0, 0);
    rect(button2x, buttony, buttonSizeX, buttonSizeY);
    fill(0);
    textSize(20);
    text("OFF", (2.8*width)/6.0, height/6.4);
  } else if (robot2 == true)
  {
    fill(0, 255, 0);
    rect(button2x, buttony, buttonSizeX, buttonSizeY);
    fill(0);
    textSize(20);
    text("ON", (2.7*width)/5.8, height/6.4);
  }
  if (robot3 == false)
  {
    fill(255, 0, 0);
    rect(button3x, buttony, buttonSizeX, buttonSizeY);
    fill(0);
    textSize(20);
    text("OFF", (4.6*width)/6.0, height/6.4);
  } else if (robot3 == true)
  {
    fill(0, 255, 0);
    rect(button3x, buttony, buttonSizeX, buttonSizeY);
    fill(0);
    textSize(20);
    text("ON", (4.5*width)/5.8, height/6.4);
  }
  
  
}

void mousePressed() {
  if (overBoxUp) 
  { 
    Uplocked = true; 
    Downlocked = false;
    Leftlocked = false;
    Rightlocked = false;
    //println("up = ", Uplocked, ", down = ", Downlocked, ", right = ", Rightlocked, ", left = ", Leftlocked);
  } else if (overBoxDown)
  {
    Downlocked = true;
    Uplocked = false; 
    Leftlocked = false;
    Rightlocked = false; 
    //println("up = ", Uplocked, ", down = ", Downlocked, ", right = ", Rightlocked, ", left = ", Leftlocked);
  } else if (overBoxLeft)
  {
    Leftlocked = true; 
    Uplocked = false; 
    Downlocked = false;
    Rightlocked = false;
    //println("up = ", Uplocked, ", down = ", Downlocked, ", right = ", Rightlocked, ", left = ", Leftlocked);
  } else if (overBoxRight)
  {
    Rightlocked = true; 
    Uplocked = false; 
    Downlocked = false;
    Leftlocked = false;
    //println("up = ", Uplocked, ", down = ", Downlocked, ", right = ", Rightlocked, ", left = ", Leftlocked);
  } 


  if (overButton1)
  {
    robot1 = !robot1;
  }
  if (overButton2)
    robot2 = !robot2;
  if (overButton3)
    robot3 = !robot3;
    
    
  if(robot1 == true)
  {
    if(Uplocked == true)
      outputs[0] = "0,20,100,100";
    else if(Downlocked == true)
      outputs[0] = "0,20,80,80";
    else if(Leftlocked == true)
      outputs[0] = "0,20,80,100";
    else if(Rightlocked == true)
      outputs[0] = "0,20,100,80";
    else
      outputs[0] = "0,20,90,90";
  }
  else
    outputs[0] = "0,20,90,90";
  
  
  if(robot2 == true)
  {
    if(Uplocked == true)
      outputs[1] = "1,20,100,100";
    else if(Downlocked == true)
      outputs[1] = "1,20,80,80";
    else if(Leftlocked == true)
      outputs[1] = "1,20,80,100";
    else if(Rightlocked == true)
      outputs[1] = "1,20,100,80";
    else
      outputs[1] = "1,20,90,90";
  }
  else
    outputs[1] = "1,20,90,90";
      
      
  if(robot3 == true)
  {
    if(Uplocked == true)
      outputs[2] = "2,20,100,100";
    else if(Downlocked == true)
      outputs[2] = "2,20,80,80";
    else if(Leftlocked == true)
      outputs[2] = "2,20,80,100";
    else if(Rightlocked == true)
      outputs[2] = "2,20,100,80";
    else
      outputs[2] = "2,20,90,90";
   
  }
   else
     outputs[2] = "2,20,90,90";
    
  for(int i = 0; i < 2; i++)
  {
    myClient.write(outputs[i]+",");   //???? is this right??
    //println(outputs[i]);
  }
}

void mouseReleased() 
{
  Uplocked = false;
  Downlocked = false;
  Leftlocked = false;
  Rightlocked = false;
  //println("up = ", Uplocked, ", down = ", Downlocked, ", right = ", Rightlocked, ", left = ", Leftlocked);
}

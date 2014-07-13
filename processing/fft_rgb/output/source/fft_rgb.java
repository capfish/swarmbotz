import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import processing.net.*; 
import processing.serial.*; 
import ddf.minim.analysis.*; 
import ddf.minim.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class fft_rgb extends PApplet {

/**

http://www.instructables.com/id/This-Is-Your-Brain-On-Music
*/
 
Client myClient;






Minim minim;
AudioInput in;
AudioPlayer song;
FFT fft;

boolean MICIN = false;

// Visualizer efaults
float valScale = 1.0f;
float maxVisible = 10.0f;
float beatThreshold = 0.25f;
float colorOffset = 30;
float autoColorOffset = 0.01f;

// Show text if recently adjusted
boolean showscale = false;
boolean showBeatThreshold = false;
boolean showHelp = false;

float beatH = 0;
float beatS = 0;
float beatB = 0;
float arduinoBeatB = 0;

float[] lastY;
float[] lastVal;

int buffer_size = 1024;  // also sets FFT size (frequency resolution)
float sample_rate = 44100;


boolean fullscreen = false;
int lastWidth = 0;
int lastHeight = 0;

String rvals, gvals, bvals;
int dropTime = 0; //drop packets 
int dropMax = 5; //every how many?



public void setup() {

  size(500, 300);
  frame.setResizable(true);
  
  myClient = new Client(this, "127.0.0.1", 5208);


  background(0);
  
  minim = new Minim(this);

  if (MICIN) {
    in = minim.getLineIn(Minim.MONO,buffer_size,sample_rate);
    fft = new FFT(in.bufferSize(), in.sampleRate());
    }
  else{
    //song = minim.loadFile("beat.mp3", 1024);
    //song = minim.loadFile("Neon Cathedral.mp3", 2048);
    song = minim.loadFile("heavyweight.mp3",2048);
    song.loop();
    fft = new FFT( song.bufferSize(), song.sampleRate() );
  }
  
  fft.logAverages(16, 2);
  fft.window(FFT.HAMMING);
  
  lastY = new float[fft.avgSize()];
  lastVal = new float[fft.avgSize()];
  initLasts();
  
  
  textSize(10);
  
  frame.setAlwaysOnTop(true);
}

public int leftBorder()   { return PApplet.parseInt(.05f * width); }
public int rightBorder()  { return PApplet.parseInt(.05f * width); }
public int bottomBorder() { return PApplet.parseInt(.05f * width); }
public int topBorder()    { return PApplet.parseInt(.05f * width); }


public void initLasts()
{
  
  for(int i = 0; i < fft.avgSize(); i++) {
    lastY[i] = height - bottomBorder();
    lastVal[i] = 0;
  }
  
}

public void draw() {
   
    colorMode(RGB);
  
    // Detect resizes
    if(width != lastWidth || height != lastHeight)
    {
      lastWidth = width;
      lastHeight = height;
      background(0);
      initLasts();
      println("resized");
    }
  
    // Slowly erase the screen
    fill(0,10 * 60/frameRate); // Based on 60fps
    rect(0,0,width,height - 0.8f*bottomBorder());
  
    colorMode(HSB, 100);
    if (MICIN){
      fft.forward(in.mix);
    }
    else{
      fft.forward(song.mix);
    }
    smooth();
    noStroke();
    
    
    int iCount = fft.avgSize();
    float barHeight =  0.03f*(height-topBorder()-bottomBorder());
    float barWidth = (width-leftBorder()-rightBorder())/iCount;
    
    float biggestValChange = 0;
    
    for(int i = 0; i < iCount; i++) {
      
      float iPercent = 1.0f*i/iCount;
      
      float highFreqscale = 1.0f + pow(iPercent, 4) * 2.0f;
      
      float val = sqrt(fft.getAvg(i)) * valScale * highFreqscale / maxVisible;
      
      float y = height - bottomBorder() - val * (height - bottomBorder() - topBorder());
      float x = leftBorder() + iPercent * (width - leftBorder() - rightBorder()) ;
      
      float h = 100 - (100.0f * iPercent + colorOffset) % 100;
      float s = 70 - pow(val, 3) * 70;
      float b = 100;
      
      fill(h, s, b);
      textAlign(CENTER, BOTTOM);
      text(nf(PApplet.parseInt(100*val),2), x+barWidth/2, y);
           
      rectMode(CORNERS);
      rect(x, y+barHeight/2, x+barWidth, lastY[i]+barHeight/2);
      
      float valDiff = val-lastVal[i];
      if(valDiff > beatThreshold && valDiff > biggestValChange)
      {
        biggestValChange = valDiff;
        beatH = h;
        beatS = s;
        beatB = b;
      }
      
      lastY[i] = y;
      lastVal[i] = val;

    }
    
    // If we've hit a beat, bring the brightness of the bar up to full
    if(biggestValChange > beatThreshold)
    {
      arduinoBeatB = 100;
    }  
    
    // calculate the arduino beat color
    int c_hsb = color(beatH, 90, constrain(arduinoBeatB, 1, 100));
    
    int r = PApplet.parseInt(red(c_hsb) / 100 * 255);
    int g = PApplet.parseInt(green(c_hsb) / 100 * 255);
    int b = PApplet.parseInt(blue(c_hsb) / 100 * 255);
   
    // clear out the message area
    fill(0);
    rect(0, height - 0.8f*bottomBorder(), width, height);
    
    
    // draw the beat bar
    colorMode(RGB, 255);
    fill(r, g, b);
    rect(leftBorder(), height - 0.8f*bottomBorder(), width-rightBorder(), height - .5f*bottomBorder());

////ARDUINO!!
    rvals = "0," + r + "," +  g + "," + b;
    gvals = "1," + r + "," +  g + "," + b;
    //bvals = "2," + blue_vals[0] + "," +  blue_vals[1] + "," + blue_vals[2];
    
  if (dropTime == dropMax){
    myClient.write(rvals + ", 90, 90");
    //myClient.write(gvals + ", 90, 90");
    //myClient.write(bvals + ", 90, 90");
    dropTime = 0;
  }
  dropTime++;
  

    // Decay the arduino beat brightness (based on 60 fps)
    arduinoBeatB *= 1.0f - 0.10f * 60/frameRate;
    //arduinoBeatB = 1.0;
    
    // Automatically advance the color
    colorOffset += autoColorOffset;
    colorOffset %= 100;

    // Show the scale if it was adjusted recently
    if(showscale)
    {
      fill(255,255,255);
      textAlign(RIGHT, TOP);
      text("scale:"+nf(valScale,1,1), width-rightBorder(), topBorder());
      showscale=false;
    }
    
    // Show the beat threshold if it was adjusted recently
    if(showBeatThreshold)
    {
      fill(255,255,255);
      textAlign(RIGHT, TOP);
      text("beat threshold:"+nf(beatThreshold,1,2), width-rightBorder(), topBorder());
      showBeatThreshold=false;
    }
     
    // Show the help
    if(showHelp)
    {
      fill(255,255,255);
      textAlign(RIGHT, TOP);
      text("Help:\nUP/DOWN arrows = Scale Visualizer\n" + 
           "LEFT/RIGHT arrows = Temporarily shift colors\n" + 
           "+/- = Beat Detection Sensitivity\n" + 
           "TAB = Use Next Arduino Port\n" + 
           "SPACE = Toggle full-screen\n" + 
           "Anything Else = Show this help", width-rightBorder(), topBorder());
      showHelp=false;
    }
     
    // Display the frame rate
    fill(16, 16, 16);
    textAlign(RIGHT, BOTTOM);
    text(nf(frameRate,2,1) + " fps", width - rightBorder(), topBorder());
    if(!fullscreen)
    {
    frame.setTitle("This Is Your Brain On Music ("+nf(frameRate,2,1)+" fps)");
    }

}

public void keyReleased()
{
  if (key == CODED)
  {
   if (keyCode == UP)
   {
     valScale += 0.1f;
     showscale=true;
   }
   else if (keyCode == DOWN)
   {
     valScale -= 0.1f;
     showscale = true;
   }
   else if (keyCode == RIGHT)
   {
     colorOffset -= 5;
   }
   else if (keyCode == LEFT)
   {
     colorOffset += 5;
   }
  }
  else
  {
    if (key == '+')
    {
      beatThreshold += 0.05f;
      showBeatThreshold=true;
    }
    else if (key == '-')
    {
      beatThreshold -= 0.05f;
      showBeatThreshold=true;
    }
    else if (key == ' ')
    {
      toggleFullScreen();
    }
    else if (key == TAB)
    {
    }
    else
    {
      showHelp = true;
    }
  } 
}

public void keyPressed()
{
  
  // In fullscreen mode, capture ESC for exiting full screen
  if (key == ESC)
  {
   if(fullscreen)
   {
     toggleFullScreen(); 
     key=0;
   }
  }
}

public void toggleFullScreen()
{
  fullscreen = !fullscreen;
  
  frame.removeNotify();
  frame.setUndecorated(fullscreen);
  if(fullscreen) {
    frame.setSize(displayWidth, displayHeight);
    frame.setLocation(0,0);
  }
  else
  {
    frame.setSize(500, 300);
    frame.setLocation(100,100);
  }
  frame.addNotify();
}

public void stop()
{
  // always close Minim audio classes when you finish with them
  if (MICIN){
    in.close();
  }
  else{
    song.close();
  }
  minim.stop();
 
  super.stop();
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "fft_rgb" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}

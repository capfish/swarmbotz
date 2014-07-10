import processing.net.*;

Client btleSocket;
PrintWriter output;

PShape dot;
int rad = 60;
int count = 0;

int bots = 3;
float[] yspeeds = new float[bots];
float[] ydeltas = new float[bots];
ArrayList<float[]> waypoints = new ArrayList<float[]>();
FloatList headings = new FloatList();
boolean[] reverseFlags = new boolean[bots];

float maxRotSpeed = 30.0;
float MAXROT_INV = (2.0/PI) * maxRotSpeed;
float maxSpeed = 30.0;
float MAXSPEED_INV = (1/10.0) * maxSpeed;
String[] RGBcmd = {"0,0,0", "0,0,0", "0,0,0"};

String[] RGB1 = {"255,255,0", "0,0,0", "0,0,0"};
String[] RGB2 = {"0,0,0", "255,0,255", "0,0,0"};
String[] RGB3 = {"0,0,0", "0,0,0", "0,255,255"};
ArrayList<String[]> RGBfoo = new ArrayList<String[]>();


void setup()
{
RGBfoo.add(RGB1);
RGBfoo.add(RGB2);
RGBfoo.add(RGB3);
  btleSocket = new Client(this, "127.0.0.1", 5207);
    output = createWriter("positions.txt"); 
    size(640, 640);
    noStroke();
    frameRate(30);
    ellipseMode(RADIUS);
    //setup initial values
    for(int i=0; i<bots; i++) {
        waypoints.add(new float[] {(i+1)*width/(bots+1), height/2});
        yspeeds[i] = -8.0;
        ydeltas[i] = 0.25;
        reverseFlags[i] = false;
        headings.append(-PI/2);
    }
   // dot = loadShape("circle-arrow-up.svg");
}

void draw()
{
  background(255,255,255);
  count = count +1;

  for(int i=0; i<bots; i++) {
       
      driveServos(btleSocket,i);
      try {
          Thread.sleep(20);
      } catch (Exception e) {
      }
  }
  if ((count > 0&&count<10)){
    RGBcmd = RGB1;
  }
  if (count >= 12&&count<20){
    RGBcmd = RGB2;
  }
  if (count >= 22&&count<30){
    RGBcmd = RGB3;
  }
  if (count > 30) {
      exit();
  }
}

void driveServos(Client socket,int botid) {
    socket.write(formatCmd(botid));
    return;
}

String formatCmd(int botid) {
    String sbotid = str(botid);
    return(sbotid + "," + RGBcmd[botid] + ",90,90");
}

float[] rotation(float dtheta) {
    float[] rotSpeed = new float[2];
    rotSpeed[0] = 90-dtheta*MAXROT_INV;
    rotSpeed[1] = 90+dtheta*MAXROT_INV;
    return rotSpeed;
}

float translate(boolean reverse, float dx, float dy) {
    float dist = sqrt(dx*dx + dy*dy);
    float transSpeed = dist * MAXSPEED_INV;
    if(reverse) {
        transSpeed = -transSpeed;
    }
    return transSpeed;
}

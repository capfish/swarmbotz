import processing.net.*;

Client btleSocket;
PrintWriter output;

PShape dot;
int rad = 60;
int count = 0;

int bots = 1;
float[] yspeeds = new float[bots];
float[] ydeltas = new float[bots];
ArrayList<float[]> waypoints = new ArrayList<float[]>();
FloatList headings = new FloatList();
boolean[] reverseFlags = new boolean[bots];

float maxRotSpeed = 30.0;
float MAXROT_INV = (2.0/PI) * maxRotSpeed;
float maxSpeed = 30.0;
float MAXSPEED_INV = (1/10.0) * maxSpeed;
//String[] RGBcmd = {"255,255,0", "255,0,255", "0,255,255"};
String SERVO_TYPE = "20";

void setup()
{
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
    dot = loadShape("circle-arrow-up.svg");
}

void draw()
{
  background(255,255,255);
  count = count +1;

  for(int i=0; i<bots; i++) {
      float xpos = waypoints.get(waypoints.size()-bots)[0];
      float ypos = waypoints.get(waypoints.size()-bots)[1];
      //creates a delay between when the robots move
      if(count > i*10) {
          if (ypos > 0 && ypos <= height/2) {
              yspeeds[i] = yspeeds[i] + ydeltas[i];
              waypoints.add(new float[] {xpos, ypos+yspeeds[i]});
          } else {
              //robot is standing still
              waypoints.add(waypoints.get(waypoints.size()-bots));
          }              
      } else {
          //robot is standing still
          waypoints.add(waypoints.get(waypoints.size()-bots));
      }
      float xpos2 = waypoints.get(waypoints.size()-1)[0];
      float ypos2 = waypoints.get(waypoints.size()-1)[1];
      float dx = xpos2 - xpos;
      float dy = ypos2 - ypos;
      float prevHeading = headings.get(headings.size()-bots);
      //atan2 returns zero if the robot hasn't moved, we don't necessarily want to rotate
      if(dy == 0 && dx == 0) {
          headings.append(prevHeading);
      } else {
          headings.append(atan2(dy, dx));
      }
      float newHeading = headings.get(headings.size()-1);
      if(reverseFlags[i]) {
          newHeading = newHeading-PI;
          headings.set(headings.size()-1,newHeading);
      }
      float deltaHeading = newHeading - prevHeading;
      if(abs(deltaHeading) > PI/2) {
          reverseFlags[i] = !reverseFlags[i];
          newHeading = prevHeading - (PI - deltaHeading);
          headings.set(headings.size()-1,newHeading);
      }
      deltaHeading = newHeading - prevHeading;
      driveServos(btleSocket, i, reverseFlags[i], dx, dy, deltaHeading);
      shape(dot,xpos2, ypos2, rad, rad);
      try {
          Thread.sleep(20);
      } catch (Exception e) {
      }
  }
  
  if (count < -1) {
      exit();
  }
}

void driveServos(Client socket, int botid, boolean reverse, float dx, float dy, float dtheta) {
    float[] rotSpeed = rotation(dtheta);
    float transSpeed = translate(reverse, dx, dy);
    float[] totalSpeed = {rotSpeed[0]+transSpeed, rotSpeed[1]+transSpeed};
    socket.write(formatCmd(botid, totalSpeed));
    return;
}

String formatCmd(int botid, float[] cmd) {
    String sbotid = str(botid);
    String leftServo = str(int(cmd[0]));
    String rightServo = str(int(cmd[1]));
    return(sbotid + "," + SERVO_TYPE + "," + leftServo + "," + rightServo);
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


// def formatCmd(botid, cmd):
//     botid = [botid]
//     finalcmd = str(botid+RGBCMD+cmd)[1:-1]
//     print finalcmd + '\n'
//     return str(finalcmd)

// def driveServos(sock, botid, reverseFlag, dx, dy, dtheta):
//     cmd = rotate(dtheta)
//     cmd2= translate(reverseFlag, dx, dy) 
//     addedCmd = [int(a+b) for a, b in zip(cmd, cmd2)]
//     sock.send(formatCmd(botid, addedCmd))
//     return(formatCmd(botid, addedCmd))

// def translate(reverseFlag, dx, dy): #at max 10 pixel jump we go full speed
//     dist = sqrt(dx**2 + dy**2)
//     cmd = [dist * MAXSPEED_INV, dist * MAXSPEED_INV]
//     if reverseFlag:
//         cmd = [-bar for bar in cmd] 
//         print 'reverse!'
//     return cmd

// def rotate(dtheta): #dtheta in radians -- a full pi/2 rotation = max speed, +- fullRotSpeed
//     # pos dtheta = rotate CCW left back right fwd
//     cmd = [90 - dtheta * MAXROT_INV, 90 + dtheta * MAXROT_INV]
//     return cmd

// def main():
    
//     fi = open("./positions-python.txt", "w")
//     host = constants.HOST_BTLE
//     port = constants.PORT_BTLE
//     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
//     NUMROBOTS = 3
//     sock.connect((host,port))

//     bots, botheadings = processwave()
//     print 'lengthbots', len(bots)
//     print 'lengthboheadingts', len(botheadings)
//     bot1, bot2, bot3 = bots
//     bot1h, bot2h, bot3h = botheadings
//     print 'bot1', bot1
//     print 'bot1h', bot1h
//     #heading: (False, 1.5707963267948966)
//     #x, y = ((160, 328)
//     for i in range(len(bot1)-2):
//         for j in range(len(bots)):
//             #(1,2) and (2,2)
//             dx, dy = [foo-bar for foo, bar in zip(bots[j][i+1],bots[j][i])]
//             reverseFlag = botheadings[j][i+1][0]
//             print i, j
//             dtheta = botheadings[j][i+1][1] - botheadings[j][i][1]
//             finalcmd = driveServos(sock, j, reverseFlag, dx,dy, dtheta)
//             fi.write(finalcmd + '\n')
//         time.sleep(.05)

//     fi.close()
//     fi = open("./positions-python-format.txt", "w")
//     data = open("./positions-python.txt", "r").readlines()
//     for n, line in enumerate(data):
//         if n%3 == 0:
//             data[n] = '\n'+line.rstrip()
//         else:
//             data[n] = line.rstrip()
//     fi.write(",".join(data))
//     fi.close()
//     sock.close()


// if __name__ == "__main__":
//     main()

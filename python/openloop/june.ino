#include <Servo.h>

//robot #1
Servo L1_serv;
Servo R1_serv;

//robot #2
Servo L2_serv;
Servo R2_serv;

//robot #3
Servo L3_serv;
Servo R3_serv;

const int neutral = 92;
const int l_forward = 180;
const int r_forward = 0;
const int l_backward = 0;
const int r_backward = 180;

int L1_speed = l_forward;
int R1_speed = r_forward;
int L2_speed = l_forward;
int R2_speed = r_forward;
int L3_speed = l_forward;
int R3_speed = r_forward;

int delta;

void setup()
{
  //not sure how to set this up... the servos are all on the same pins for the robots.. how to differentiate? 
}


//wave motion
void loop()
{
  //starting from a line up of robot 1,2,3
  delta = 5; 
  
  if(L1_speed >= l_backward || R1_speed <= r_backward)
  {
    L1_speed = L1_speed -delta; 
    R1_speed = R1_speed + delta;
    
    L1_serv.write(L1_speed);
    R1_serv.write(R1_speed);
  }
  
  if(//amount of time since the function was called > x amount of time)
  {
    if(L2_speed >= l_backward || R2_speed <= r_backward)
    {
      L2_speed = L2_speed -delta;
      R2_speed = R2_speed + delta;

      L2_serv.write(L2_speed);
      R2_serv.write(R2_speed);
    }
  }
  
  if(//amount of time since the function was called > 2*x amount of time)
  {
    if(L3_speed >= l_backward || R3_speed <= r_backward)
    {
      L3_speed = L3_speed - delta;
      R3_speed = R3_speed + delta;
      
      L3_serv.write(L3_speed);
      R3_serv.write(R3_speed);
    }
  }
}

void circle()
{
  //starting from a line up of robot 1,2,3
  L2_serv.write(l_forward);
  R2_serv.write(r_forward); 
  delay(?); // until robot 1,2,3 make an equilateral triangle
  
  L1_serv.write(1_backward);
  R1_serv.write(r_forward);
  delay(?); //until robot turns 90degree left
  
  L3_serv.write(l_forward);
  R3_serv.write(r_backward);
  delay(?); //until robot turns 180degree
  
  L1_serv.write(1_forwad);
  R1_serv.write(r_backward);
  L2_serv.write(l_forward);
  R2_serv.write(r_backward);
  L3_serv.write(1_forward);
  R3_serv.write(r_backward);
  delay(?)//until robots turn 45degree right
  
  // now in position for robots to move in circles
  //the speeds of the left and right servos need to be adjusted to make a circular motion
  
  for(int i = 0; i <= 360; i++)
  {
    float j = cos((3.14*i)/180);
    float k = sin((3.14*i)/180);
    //CIRCULAR MOTION?!!?! math cannot do.. terrible terrible
  
  }
  
}

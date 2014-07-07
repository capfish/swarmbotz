boolean useVFlip = true;
import megamu.shapetween.*;

Tween ani;
void setup(){
  ani = new Tween(this, 2, Tween.SECONDS, Shaper.COSINE);
  Tween.timeScale = .5;
  ani.start();
}

void draw(){
  //switch to 0,0 in bottom left
  scale(1,-1);
  translate(0,-height);
  
  background(255);
  ellipse(ani.time()*width, ani.position()*height, 4, 4);
  println(ani.time() +", " +ani.position());
}

//
//import megamu.shapetween.*;
//
//Tween ani;
//void setup(){
//// Tween( parent, duration, durationType, easing )=
//  ani = new Tween(this, 2, Tween.SECONDS, Shaper.COSINE);
//}
//
//void draw(){
//  background(255);
//  //ellipse(x,y, x width, y width)
//  ellipse(ani.time()*width, ani.position()*height, 4, 4);
//  //print(ani.time() + ani.position());
//}


//boolean useVFlip = true;
//import megamu.shapetween.*;
//
//Tween ani;
//void setup(){
//  ani = new Tween(this, 2, Tween.SECONDS, Shaper.COSINE);
//  Tween.timeScale = .5;
//  ani.start();
//}
//
//void draw(){
//  //switch to 0,0 in bottom left
//  scale(1,-1);
//  translate(0,-height);
//  
//  background(255);
//  ellipse(ani.time()*width, ani.position()*height, 4, 4);
//  println(ani.time() +", " +ani.position());
//}



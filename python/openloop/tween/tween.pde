import ijeoma.motion.*;
import ijeoma.motion.tween.*;

Tween t;

float w = 0;

void setup() {
  size(400, 400);
  smooth();

  Motion.setup(this);

  t = new Tween(this, "w", width, 100);
  //t = new Tween(100).add(this, "w",100);
}

void draw() {
    //switch to 0,0 in bottom left
  scale(1,-1);
  translate(0,-height);
  
  background(255);

  noStroke();

  fill(255 / 2f);
  ellipse(10,w, 10,10);

  String time = t.getTime() + " / " + t.getDuration();

  fill(0);
  text(time, width - textWidth(time) - 10, height - 10);
  println("w"+w);
}

void keyPressed() {
  t.play();
}

void tweenStarted(Tween _t) {
  println(_t + " started");
}

void tweenEnded(Tween _t) {
  println(_t + " ended");
}

// void tweenChanged(Tween _t) {
// println(_t + " changed");
// }

void tweenRepeated(Tween _t) {
  println(_t + " repeated");
} 

void mousePressed() {
  w = mouseX;
}

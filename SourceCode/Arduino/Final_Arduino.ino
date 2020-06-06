#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int16.h>
#include <std_msgs/UInt16.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <L3G.h>

int motorright = 9;                                                              
int motorrightdir  = 7;
int motorleft = 10;
int motorleftdir  = 8;

class BlueROS : public ArduinoHardware
{
  protected:

  private:
    SoftwareSerial *mySerial;
  public:
  BlueROS(){}

  void init(){
    mySerial = new SoftwareSerial(A0, 11);
    mySerial->begin(57600);
  }

  int read(){
    return mySerial->read();
  };
  
  void write(uint8_t* data, int length){
    for(int i=0; i<length; i++){
      mySerial->write(data[i]);
    }
  }
};

ros::NodeHandle_<BlueROS, 3, 5, 100, 100> nh;

void ros_handler(const geometry_msgs::Twist& cmd_msg){
  float x = cmd_msg.linear.x;
  float y = cmd_msg.linear.y;
  float z = cmd_msg.linear.z;
  if(x == -1.0) backward(1000);
  if(x == 1.0) forward(1000);
  if(y == -1.0) right(1000);
  if(y == 1.0) left(1000);
  stop();
}

ros::Subscriber<geometry_msgs::Twist> sub("/zumo/cmd_vel", ros_handler);
std_msgs::UInt16 msgLight;
ros::Publisher pubLight("/zumo/redSig", &msgLight);
void setup() {
  Serial.begin(57600);
  
  nh.initNode();
  
  nh.subscribe(sub);
  
  nh.advertise(pubLight);
}

void loop() {
  msgLight.data = 0;
  if(Serial.available()) {
    int r = 1;
    r = r * (Serial.read() - '0');
    msgLight.data = r;
  }
  pubLight.publish(&msgLight);
  
  nh.spinOnce();
  delay(100);
}

void forward(int time)
{
  digitalWrite(motorrightdir, LOW);
  analogWrite(motorright,180); 
  digitalWrite(motorleftdir, LOW);
  analogWrite(motorleft, 180); 
  delay(time);
  stop();
}

void backward(int time)
{
  digitalWrite(motorrightdir, HIGH);
  analogWrite(motorright,180); 
  digitalWrite(motorleftdir, HIGH);
  analogWrite(motorleft, 180);
  delay(time);
  stop();
}

void left(int time)
{
  digitalWrite(motorrightdir, LOW);
  analogWrite(motorright,120); 
  digitalWrite(motorleftdir, HIGH);
  analogWrite(motorleft, 120);
  delay(time);
  stop();
}

void right(int time)
{
  digitalWrite(motorrightdir, HIGH);
  analogWrite(motorright,120); 
  digitalWrite(motorleftdir, LOW);
  analogWrite(motorleft, 120);
  delay(time);
  stop();
}

void stop()
{
  analogWrite(motorright, 0); 
  analogWrite(motorleft, 0); 
}

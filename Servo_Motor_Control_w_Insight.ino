/*  
  These drivers use I2C to communicate, 2 pins are required to  
  interface.
  Control Prosthetic Hand with Servo Motors
  Author: Tim Murray & Mary Fennessey
*/
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <Keyboard.h>
char InsightData;
// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(&Wire, 0x40);

void setup() {
  Serial.begin(9600);
  //Serial.println("5 channel Servo test!");
  pwm.begin();
  pwm.setPWMFreq(50);  // Analog servos run at ~50 Hz updates
  for( int i = 0; i < 6; i++){
  setServoPulse(i,0.001);
  }
  delay(10);
  }

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 50;   // 50 Hz
  //Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  //Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000000;  // convert to us
  pulse /= pulselength;
  //Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}

void loop() {
  // Drive each servo at the same time
  //delay(1000);//Pauses one second (Insert sense method here)
  if(Serial.available() > 0){
    InsightData = Serial.read();//Read byte from python, translate into either a 'High' to contract hand, or 'Low' to release hand
    if(InsightData == '1'){
      Serial.print("Turn Motor On");
      for (int i = 0; i < 6; i++){//Moves all servos to 0 degress
      setServoPulse(i,.001);
      }
      delay(1000);
      for (int i = 0; i < 6; i++){//Moves all servos to 180 degrees
      setServoPulse(i,.002);
      }
      delay(1000);
    }
   else if(InsightData == '0'){
   //delay(1000);
      Serial.print("Turn Motor Off");
      for (int i = 0; i < 6; i++){//Moves all servos to 180 degrees
      setServoPulse(i,.002);
      }
    }
  }
}

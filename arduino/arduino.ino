#include "serial_handler.h"

// modules
SerialHandler serialh;

// Motor 1
#define MOTOR1A 9
#define MOTOR1B 10
// Motor 2
#define MOTOR2A 7
#define MOTOR2B 8

int motor1_prev = 0;
int motor2_prev = 0;

// motor1 is left, motor2 is right
void setMotorSpeeds(int motor1, int motor2) {
  analogWrite(MOTOR1A, (motor1 < 0) ? (0) : (motor1));
  analogWrite(MOTOR1B, (motor1 < 0) ? (-motor1) : (0));

  analogWrite(MOTOR2A, (motor2 < 0) ? (0) : (motor2));
  analogWrite(MOTOR2B, (motor2 < 0) ? (-motor2) : (0));
}

void setup() {
  Serial.begin(9600);

  pinMode(MOTOR1A, OUTPUT);
  pinMode(MOTOR1B, OUTPUT);
  pinMode(MOTOR2A, OUTPUT);
  pinMode(MOTOR2B, OUTPUT);

  analogWrite(MOTOR1A, 0);
  digitalWrite(MOTOR1B, LOW);
  digitalWrite(MOTOR2A, LOW);
  digitalWrite(MOTOR2B, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    serialh.sendMsg("received: " + data);
    // convert to float
    float f_data = atof(data.c_str());

    // couldn't detect
    if (f_data == -1.0) {
      serialh.sendMsg("can't see, stopping");
      setMotorSpeeds(0, 0);
      return;
    }

    // out of range
    if ((f_data < 5) || (f_data > 120)) {
      setMotorSpeeds(motor1_prev, motor2_prev);
      return;
    }

    // range conditions
    if (f_data > 33) {
      serialh.sendMsg("go forward");
      motor1_prev = 80;
      motor2_prev = 80;
      setMotorSpeeds(motor1_prev, motor2_prev);  
    }
    else if (f_data < 27) {
      serialh.sendMsg("go backward");
      motor1_prev = -80;
      motor2_prev = -80;
      setMotorSpeeds(motor1_prev, motor2_prev);
    }
    else {
      serialh.sendMsg("stay still");
      motor1_prev = 0;
      motor2_prev = 0;
      setMotorSpeeds(motor1_prev, motor2_prev);
    }
  }
}

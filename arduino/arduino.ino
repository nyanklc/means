int MOTOR_1 = 10;
int MOTOR_2 = 11;

void setup() {
  Serial.begin(9600);
  pinMode(MOTOR_1, OUTPUT);
  pinMode(MOTOR_2, OUTPUT);
  digitalWrite(MOTOR_1, LOW);
  digitalWrite(MOTOR_2, LOW);
}

void loop() {
    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      Serial.print("read, " + data);
      if(data == "0/n")
      {
        digitalWrite(MOTOR_1, HIGH);
        digitalWrite(MOTOR_2, LOW);
      }
      else if(data == "1/n")
      {
        digitalWrite(MOTOR_1, LOW);  
        digitalWrite(MOTOR_2, HIGH);
      }
      else
      {
        digitalWrite(MOTOR_1, LOW);
        digitalWrite(MOTOR_2, LOW); 
      }
    }
    
}

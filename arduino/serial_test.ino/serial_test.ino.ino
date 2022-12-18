int MotorPin1=7;
int MotorPin2=8;
int MotorPin3=9;
int MotorPin4=10;

void setup() { // the setup function runs only once when power on the board or reset the board:
  Serial.begin(9600);
  pinMode(MotorPin1, OUTPUT);
  pinMode(MotorPin2, OUTPUT);
  pinMode(MotorPin3, OUTPUT);
  pinMode(MotorPin4, OUTPUT);
}

void loop() {

    if (Serial.available() > 0) 
    {
    String data = Serial.readStringUntil('\n');
    float distance = atof(data.c_str());
    Serial.print("You sent me: ");
    Serial.println(distance);
    }
}

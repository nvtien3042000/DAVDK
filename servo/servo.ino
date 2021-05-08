#include<Servo.h>
Servo servo;

int signalEsp = 12;
int servoPin = 11;
int led = 13;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  servo.attach(servoPin);
  pinMode(signalEsp, INPUT);
  pinMode(led, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
  if(digitalRead(signalEsp)==HIGH){
    Serial.println("HIGH");
    servo.write(-90);
    digitalWrite(led, HIGH);
  }else{
    digitalWrite(led, LOW);
    servo.write(90);
    Serial.println("LOW");
  }
}

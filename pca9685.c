#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver srituhobby = Adafruit_PWMServoDriver();

#define servoMIN 150  // Minimum pulse width for servo
#define servoMAX 600  // Maximum pulse width for servo
#define delayTime 25 // Delay time in milliseconds for each degree

void setup() {
  Serial.begin(9600);
  srituhobby.begin();
  srituhobby.setPWMFreq(60);  // Set PWM frequency to 60Hz (standard for servos)
}

void loop() {
  // Move servo on Channel 0 from 0 to 180 degrees and back
  moveServo(0, servoMIN, servoMAX);
  delay(1000); // Wait for 1 second before starting the next movement
  
  // Move servo on Channel 1 from 0 to 180 degrees and back
  moveServo(1, servoMIN, servoMAX);
  delay(1000); // Wait for 1 second before starting the next movement
}

void moveServo(int channel, int minPulse, int maxPulse) {
  // Move servo from 0 to 180 degrees (min to max pulse width)
  for (int pulse = minPulse; pulse <= maxPulse; pulse++) {
    srituhobby.setPWM(channel, 0, pulse);  // Set PWM value for the channel
    Serial.print("Channel ");
    Serial.print(channel);
    Serial.print(" Moving to ");
    Serial.println(pulse);
    delay(delayTime);  // Delay for smooth movement (100 ms for each degree)
  }

  // Reverse movement from 180 to 0 degrees (max to min pulse width)
  for (int pulse = maxPulse; pulse >= minPulse; pulse--) {
    srituhobby.setPWM(channel, 0, pulse);  // Set PWM value for the channel
    Serial.print("Channel ");
    Serial.print(channel);
    Serial.print(" Moving to ");
    Serial.println(pulse);
    delay(delayTime);  // Delay for smooth movement (100 ms for each degree)
  }
}

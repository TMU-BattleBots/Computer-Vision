/*
Created by: Amyn Jiwani
Date Last Modified: May 24, 2026
Description: Arduino motor controller for Pi-driven vision guidance.

The Raspberry Pi sends either one PWM value (applied to both motors) or two
comma-separated PWM values in the form "left,right\n".
The controller applies the values to the ESC channels immediately and stops
the motors if no valid command has been received recently.
*/

#include <Servo.h>

const int SPEED_STOP = 1500;
const unsigned long COMMAND_TIMEOUT_MS = 500;

Servo motor1;
Servo motor2;

char inputBuffer[32];
size_t inputLength = 0;
unsigned long lastCommandMs = 0;

void applyMotorValues(int leftMicroseconds, int rightMicroseconds) {
  motor1.writeMicroseconds(leftMicroseconds);
  motor2.writeMicroseconds(rightMicroseconds);
  lastCommandMs = millis();
  Serial.print("Motors set to: ");
  Serial.print(leftMicroseconds);
  Serial.print(",");
  Serial.println(rightMicroseconds);
}

void stopMotors() {
  applyMotorValues(SPEED_STOP, SPEED_STOP);
}

void setup() {
  Serial.begin(9600);
  motor1.attach(9);
  motor2.attach(10);
  stopMotors();
  Serial.println("Arduino motor controller ready.");
}

void handleCommandLine(char *line) {
  char *comma = strchr(line, ',');
  if (comma != NULL) {
    *comma = '\0';
    int leftValue = atoi(line);
    int rightValue = atoi(comma + 1);
    if (leftValue >= 1000 && leftValue <= 2000 && rightValue >= 1000 && rightValue <= 2000) {
      applyMotorValues(leftValue, rightValue);
    }
    return;
  }

  int singleValue = atoi(line);
  if (singleValue >= 1000 && singleValue <= 2000) {
    applyMotorValues(singleValue, singleValue);
  }
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      inputBuffer[inputLength] = '\0';
      handleCommandLine(inputBuffer);
      inputLength = 0;
      continue;
    }

    if (inputLength < sizeof(inputBuffer) - 1) {
      inputBuffer[inputLength++] = c;
    }
  }

  if (millis() - lastCommandMs > COMMAND_TIMEOUT_MS) {
    stopMotors();
  }
}
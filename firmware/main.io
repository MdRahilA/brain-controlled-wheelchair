// firmware/mcu/src/main.ino
// =====================================
// Brain-Controlled Wheelchair Firmware
// =====================================

#define LEFT_MOTOR_FWD  5
#define LEFT_MOTOR_REV  6
#define RIGHT_MOTOR_FWD 9
#define RIGHT_MOTOR_REV 10

unsigned long lastCommandTime = 0;
const unsigned long timeoutMs = 3000; // 3 sec safety stop

void setup() {
  Serial.begin(9600);
  pinMode(LEFT_MOTOR_FWD, OUTPUT);
  pinMode(LEFT_MOTOR_REV, OUTPUT);
  pinMode(RIGHT_MOTOR_FWD, OUTPUT);
  pinMode(RIGHT_MOTOR_REV, OUTPUT);
  stopMotors();
  Serial.println("MCU Ready. Awaiting serial commands...");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    handleCommand(cmd);
    lastCommandTime = millis();
  }

  // Safety stop if no command received
  if (millis() - lastCommandTime > timeoutMs) {
    stopMotors();
  }
}

void handleCommand(String cmd) {
  if (cmd == "FWD") forward();
  else if (cmd == "LEFT") turnLeft();
  else if (cmd == "RIGHT") turnRight();
  else if (cmd == "STOP") stopMotors();
  else Serial.println("Unknown command");
}

void forward() {
  analogWrite(LEFT_MOTOR_FWD, 200);
  analogWrite(RIGHT_MOTOR_FWD, 200);
  analogWrite(LEFT_MOTOR_REV, 0);
  analogWrite(RIGHT_MOTOR_REV, 0);
  Serial.println("Moving forward");
}

void turnLeft() {
  analogWrite(LEFT_MOTOR_FWD, 0);
  analogWrite(RIGHT_MOTOR_FWD, 200);
  analogWrite(LEFT_MOTOR_REV, 0);
  analogWrite(RIGHT_MOTOR_REV, 0);
  Serial.println("Turning left");
}

void turnRight() {
  analogWrite(LEFT_MOTOR_FWD, 200);
  analogWrite(RIGHT_MOTOR_FWD, 0);
  analogWrite(LEFT_MOTOR_REV, 0);
  analogWrite(RIGHT_MOTOR_REV, 0);
  Serial.println("Turning right");
}

void stopMotors() {
  analogWrite(LEFT_MOTOR_FWD, 0);
  analogWrite(RIGHT_MOTOR_FWD, 0);
  analogWrite(LEFT_MOTOR_REV, 0);
  analogWrite(RIGHT_MOTOR_REV, 0);
  Serial.println("Stopped");
}

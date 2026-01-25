#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "ESP32CAM_AP";
const char* password = "";

WiFiUDP udp;
unsigned int localPort = 5005;
char incoming[255];

// Ultrasound sensor pins
#define TRIG_PIN D2
#define ECHO_PIN D3

long duration;
float distance;

// Driver OUT pins
#define L_PWM D9
#define L_DIR D10
#define R_PWM D11
#define R_DIR D12

const int BASE_SPEED = 1200;
const int PWM_FREQ = 20000;
const int PWM_RES = 11;

void printDistance(int distance) {
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.print("cm\n");
}

void printPacket(int steer) {
  Serial.print("Packet: ");
  Serial.print(steer);
  Serial.print("\n");
}

void setMotor(int pwmPin, int dirPin, int channel, int speed) {
  speed = constrain(speed, 0, 2000);

  digitalWrite(dirPin, LOW);
  ledcWrite(channel, speed);
}

void driveSteering(int steer) {
  if (abs(steer) < 50) steer = 0;

  int left = BASE_SPEED - steer;
  int right = BASE_SPEED + steer;

  setMotor(L_PWM, L_DIR, 0, left);
  setMotor(R_PWM, R_DIR, 1, right);
}

void stopWheels() {
  setMotor(L_PWM, L_DIR, 0, 0);
  setMotor(R_PWM, R_DIR, 1, 0);
}

void setup() {
  Serial.begin(115200);
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(L_DIR, OUTPUT);
  pinMode(R_DIR, OUTPUT);

  ledcSetup(0, PWM_FREQ, PWM_RES);
  ledcSetup(1, PWM_FREQ, PWM_RES);

  ledcAttachPin(L_PWM, 0);
  ledcAttachPin(R_PWM, 1);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.print("WiFi Connected");

  udp.begin(localPort);
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incoming, 255);
    if (len > 0) incoming[len] = 0;
  }
  const int steer = atoi(incoming) - 1000;

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.0343 / 2;

  printDistance(distance);
  printPacket(steer);

  if (distance < 5 || steer > 2000) {
    stopWheels();
  } else {
    driveSteering(steer);
  }

  delay(200);
}

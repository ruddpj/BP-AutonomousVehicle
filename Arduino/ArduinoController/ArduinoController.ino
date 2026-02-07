#include <WiFi.h>
#include <WiFiUdp.h>

// WiFi Settings + UDP Buffer
const char* ssid = "LAPTOP_AP";
const char* password = "12345678";

WiFiUDP udp;
unsigned int localPort = 5005;
uint8_t incoming[2];
int steer = -256;

// Ultrasound sensor pins
#define TRIG_PIN D2
#define ECHO_PIN D3

// Ultrasound variables
volatile uint32_t echoStart = 0;
volatile uint32_t echoEnd = 0;
volatile bool echoDone = false;
float distance = 0;

// Driver OUT pins
#define L_PWM D9
#define L_DIR D10
#define R_PWM D5
#define R_DIR D6

// Driver constants
const int BASE_SPEED = 255;
const int PWM_FREQ = 20000;
const int PWM_RES = 8;

// Print-outs
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

// Motor Functions
void setMotor(int pwmPin, int dirPin, int channel, int speed) {
  if (speed < 0) {
    digitalWrite(dirPin, HIGH);
    speed = -speed;
  } else {
    digitalWrite(dirPin, LOW);
  }

  ledcWrite(channel, constrain(speed, 0, 255));
}

void driveSteering(int steer) {
  if (steer > -16 && steer < 16) steer = 0;

  int left = constrain(BASE_SPEED - steer * 2, -255, 255);
  int right = constrain(BASE_SPEED + steer * 2, -255, 255);

  setMotor(L_PWM, L_DIR, 0, left);
  setMotor(R_PWM, R_DIR, 1, right);
}

void stopWheels() {
  ledcWrite(0, 0);
  ledcWrite(1, 0);
}

// Ultrasound control functions
void IRAM_ATTR echoISR() {
  if (digitalRead(ECHO_PIN)) {
    echoStart = micros();
  } else {
    echoEnd = micros();
    echoDone = true;
  }
}

void triggerUltrasonic() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
}

void setup() {
  Serial.begin(115200);
  
  // Ultrasound setup
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  attachInterrupt(ECHO_PIN, echoISR, CHANGE);

  // Setup direction pins
  pinMode(L_DIR, OUTPUT);
  pinMode(R_DIR, OUTPUT);

  digitalWrite(L_DIR, LOW);
  digitalWrite(R_DIR, LOW);

  // Setup PWM pins
  ledcSetup(0, PWM_FREQ, PWM_RES);
  ledcSetup(1, PWM_FREQ, PWM_RES);

  ledcAttachPin(L_PWM, 0);
  ledcAttachPin(R_PWM, 1);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(200);
  }

  //Serial.print("WiFi Connected");
  //Serial.print(WiFi.localIP());

  udp.begin(localPort);
}

void loop() {
  while (udp.parsePacket() >= 2) {
    udp.read(incoming, 2);

    uint16_t raw = incoming[0] | (incoming[1] << 8);
    steer = (int)raw - 256;
  }

  static unsigned long lastTrig = 0;
  if (millis() - lastTrig > 50) {
    lastTrig = millis();
    echoDone = false;
    triggerUltrasonic();
  }

  if (echoDone) {
    uint32_t duration = echoEnd - echoStart;
    distance = duration * 0.0343 / 2;
    echoDone = false;
  }

  //printDistance(distance);
  //printPacket(steer);

  if (distance < 10 || steer < -255 || steer > 255) {
    stopWheels();
  } else {
    driveSteering(steer);
  }
}

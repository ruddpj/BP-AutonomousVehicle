#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "ESP32CAM_AP";
const char* password = "";

WiFiUDP udp;
unsigned int localPort = 5005;
char incoming[255];

// ---- Ultrazvukový senzor ----
#define TRIG_PIN D4   // uprav podľa zapojenia
#define ECHO_PIN D2  // uprav podľa zapojenia

long duration;
float distance;

void setup() {
  Serial.begin(115200);
  
  // Nastavenie pinov senzora
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Pripojenie k WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to AP");

  // Spustenie UDP
  udp.begin(localPort);
  Serial.printf("Listening on UDP port %d\n", localPort);
}

void loop() {
  // ---- Príjem UDP správ ----
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incoming, 255);
    if (len > 0) incoming[len] = 0;
    Serial.print("Received: ");
    Serial.println(incoming);
  }

  // ---- Meranie vzdialenosti ----
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.0343 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // ---- Ak je bližšie než 5 cm, vypíš STOP ----
  if (distance > 0 && distance < 5) {
    Serial.println("STOP");
  }

  delay(200);
}

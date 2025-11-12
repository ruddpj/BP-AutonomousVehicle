#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "ESP32CAM_AP";
const char* password = "";

WiFiUDP udp;
unsigned int localPort = 5005;
char incoming[255];

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to AP");
  udp.begin(localPort);
  Serial.printf("Listening on UDP port %d\n", localPort);
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incoming, 255);
    if (len > 0) incoming[len] = 0;
    Serial.print("Received: ");
    Serial.println(incoming);
  }
}

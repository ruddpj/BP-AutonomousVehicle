#include "esp_camera.h"
#include <WiFi.h>
#include "esp_timer.h"
#include "Arduino.h"
#include "esp_http_server.h"

// ---------------- Wi-Fi ----------------
const char* ssid = "LAPTOP_AP";
const char* password = "12345678";

// ---------------- Kamera ----------------
// Piny pre ESP32-CAM (AI-Thinker)
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// ---------------- Funkcie ----------------
httpd_handle_t stream_httpd = NULL;

// Stream handler
esp_err_t stream_handler(httpd_req_t *req){
  camera_fb_t * fb = NULL;
  char * part_buf[64];
  static const char* _STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=frame";

  httpd_resp_set_type(req, _STREAM_CONTENT_TYPE);

  while(true){
    fb = esp_camera_fb_get();
    if(!fb){
      httpd_resp_send_500(req);
      return ESP_FAIL;
    }

    // HTTP multipart
    httpd_resp_send_chunk(req, "--frame\r\n", 9);
    sprintf((char*)part_buf, "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n", fb->len);
    httpd_resp_send_chunk(req, (const char*)part_buf, strlen((char*)part_buf));
    httpd_resp_send_chunk(req, (const char*)fb->buf, fb->len);
    httpd_resp_send_chunk(req, "\r\n", 2);

    esp_camera_fb_return(fb);
    delay(30); // ~30 FPS
  }

  return ESP_OK;
}

// Spustenie HTTP stream servera
void startCameraServer(){
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();
  config.server_port = 81; // port streamu

  if(httpd_start(&stream_httpd, &config) == ESP_OK){
    httpd_uri_t stream_uri = {
      .uri       = "/stream",
      .method    = HTTP_GET,
      .handler   = stream_handler,
      .user_ctx  = NULL
    };
    httpd_register_uri_handler(stream_httpd, &stream_uri);
  }
}

// ---------------- Setup ----------------
void setup() {
  Serial.begin(115200);

  // Wi-Fi
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
  }

  // Kamera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if(psramFound()){
    config.frame_size = FRAMESIZE_QVGA;
    config.jpeg_quality = 12;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_QVGA;
    config.jpeg_quality = 15;
    config.fb_count = 1;
  }

  if(esp_camera_init(&config) != ESP_OK){
    return;
  }

  // Spustenie streamu
  startCameraServer();
}

void loop() {
  delay(1000);
}

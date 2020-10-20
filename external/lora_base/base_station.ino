/*
 * Base Station
 * Receives data over lora and processes it for display
*/
#include "heltec.h"
#include <WiFi.h>
#include <HTTPClient.h>

#define BAND    915E6  //you can set band here directly,e.g. 433E6,868E6,915E6

//---------------------- START Display ----------------------//
/*
 * Clears display and prints new message
 * This is completely optional and mostly for debugging
 * you can remove this if you do not have a 
 * Heltec device with a display
*/
void print_to_display(String first_line, String second_line = "", String third_line = "", String fourth_line = ""){
  Heltec.display->clear();
  Heltec.display->drawString(0, 0, first_line);
  Heltec.display->drawString(0, 10, second_line);
  Heltec.display->drawString(0, 20, third_line);
  Heltec.display->drawString(0, 30, fourth_line);
  Heltec.display->display();
};


/*
 * Initialie the Display
 * (optional)
*/
void initialize_display(){
  Heltec.display->init();
  Heltec.display->flipScreenVertically();  
  Heltec.display->setFont(ArialMT_Plain_10);
};

//---------------------- END Display ------------------------//

//---------------------- START LoRa -------------------------//
/*
 * Setup lora for receive
 * and inturrupt
*/
void setup_lora(){
  Heltec.begin(true /*DisplayEnable Enable*/, true /*LoRa Disable*/, true /*Serial Enable*/, true /*PABOOST Enable*/, BAND /*long BAND*/);
};


int packetNumber = 0;
/*
 * callback when a packet is received
*/
void onReceive()
{
  packetNumber++;

  //just to avoid overflow
  //this number is just for debugging
  if (packetNumber > 500){
    packetNumber = 0;
  }
  
  // received a packet
  String packetData;
  int i = 0;

  // read packet
  while (LoRa.available())
  {
    packetData += String((char)LoRa.read());
  }

  display_lora_results(packetNumber, packetData, LoRa.packetRssi());
  save_data(packetData, LoRa.packetRssi());
};

//---------------------- END LoRa -------------------------//

//---------------------- START WiFi -------------------------//
const char* ssid     = "Bradlowski";
const char* password = "Br@d-Br@dl0wsk1";
const String api_endpoint = "http://10.0.0.69/api/";

/*
 * Sets up and connects to the wifi
*/
void setup_wifi(){
  WiFi.begin(ssid, password);
  String connectStatus = "Connecting";
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      connectStatus += ".";
      print_to_display("Trying: " + String(ssid), connectStatus);
  }

  print_to_display("WiFi connected", "IP address: " + String(WiFi.localIP()));

};

/*
 * Send Data to API
*/
void save_data(String packetData, int packetRSSI){
  HTTPClient http;

  http.begin(api_endpoint + packetData); 
  
  http.addHeader("Content-Type", "text/plain");

  Serial.println(api_endpoint + packetData);
  int responce = http.POST("");
  Serial.println("Responce: " + String(responce));

  // Free resources
  http.end();
}

//---------------------- END WiFi -------------------------//

//---------------------- START Main -------------------------//
void setup() {
 setup_lora();
 initialize_display();
 setup_wifi();
};

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    onReceive();
  }
};
//---------------------- END Main -------------------------//
//---------------------- START Helper Functions -------------------------//

/*
 * This is where we display the results to the screen
 * mostly for debugging purposes.
*/
void display_lora_results(int packetNumber, String packetData, int packetRSSI){
  String WiFiDevices = "No WiFi Found.";
  String BlueToothDevices = "No BLE Found.";
  
  if (packetData.indexOf("W") > -1) {
    WiFiDevices = "WiFi Devices Found!";
  }

  if (packetData.indexOf("B") > -1) {
    BlueToothDevices = "Bluetooth Devices Found!";
  }
  print_to_display("Received packet (" + String(packetNumber) + "): ", WiFiDevices, BlueToothDevices, "RSSI: " + String(packetRSSI));
}
//---------------------- END Helper Functions -------------------------//

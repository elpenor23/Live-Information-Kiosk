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
void print_to_display(String first_line, String second_line = "", String third_line = "", String fourth_line = "", String fifth_line = "", String sixth_line = ""){

  Serial.println(first_line);
  if (second_line != ""){
    Serial.println(second_line);
  }
  if (third_line != ""){
    Serial.println(third_line);
  }
  if (fourth_line != ""){
    Serial.println(fourth_line);
  }
  if (fifth_line != ""){
    Serial.println(fifth_line);
  }
  if (sixth_line != ""){
    Serial.println(sixth_line);
  }
  
  Heltec.display->clear();
  Heltec.display->drawString(0, 0, first_line);
  Heltec.display->drawString(0, 10, second_line);
  Heltec.display->drawString(0, 20, third_line);
  Heltec.display->drawString(0, 30, fourth_line);
  Heltec.display->drawString(0, 40, fifth_line);
  Heltec.display->drawString(0, 50, sixth_line);
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
  if (packetNumber > 1000){
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

  String save_results = save_data(packetData, LoRa.packetRssi());
  display_results(packetNumber, packetData, LoRa.packetRssi(), save_results);
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
  String connectStatus = "Connecting to WiFi.";
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      connectStatus += ".";
      print_to_display("Trying: " + String(ssid), connectStatus);
  }

  IPAddress ip = WiFi.localIP();
  
  print_to_display("WiFi connected", "IP address: " + FormatIPAddress(ip));

};

/*
 * Formats IP Address for humans
*/
String FormatIPAddress(const IPAddress& ipAddress)
{
  return String(ipAddress[0]) + String(".") +\
  String(ipAddress[1]) + String(".") +\
  String(ipAddress[2]) + String(".") +\
  String(ipAddress[3])  ;
}

/*
 * Send Data to API
*/
String save_data(String packetData, int packetRSSI){
  if (WiFi.status() != WL_CONNECTED){
    setup_wifi();
  }
  
  HTTPClient http;

  http.begin(api_endpoint + packetData); 
  
  http.addHeader("Content-Type", "text/plain");

  int responce = http.POST("");

  // Free resources
  http.end();

  return api_endpoint + packetData + "|" + String(responce);
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
void display_results(int packetNumber, String packetData, int packetRSSI, String save_data){
  String WiFiDevices = "No WiFi Found.";
  String BlueToothDevices = "No BLE Found.";
  
  if (packetData.indexOf("W") > -1) {
    WiFiDevices = "WiFi Devices Found!";
  }

  if (packetData.indexOf("B") > -1) {
    BlueToothDevices = "Bluetooth Devices Found!";
  }

  int indexOfPipe = save_data.indexOf("|");
  String api_call = save_data.substring(0, indexOfPipe);
  String response_data = "Response:" + save_data.substring(indexOfPipe+1);
  
  print_to_display("Received packet (" + String(packetNumber) + "): ", WiFiDevices, BlueToothDevices, "RSSI: " + String(packetRSSI), api_call, response_data);
}
//---------------------- END Helper Functions -------------------------//

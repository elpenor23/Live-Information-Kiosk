/*
 * Detects people by scanning for bluetooth devices or wifi devices
*/

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include "heltec.h"
#include <time.h>
#include <WiFi.h>
#include "esp_wifi.h"

//-------------------- Start WiFi ---------------------------//
#define maxCh 11 //max Channel -> US = 11, EU = 13, Japan = 14
int numWiFiDevicesFound = 0;

const wifi_promiscuous_filter_t filt={ //Idk what this does
    .filter_mask=WIFI_PROMIS_FILTER_MASK_MGMT|WIFI_PROMIS_FILTER_MASK_DATA
};

typedef struct { // or this
  uint8_t mac[6];
} __attribute__((packed)) MacAddr;

typedef struct { // still dont know much about this
  int16_t fctl;
  int16_t duration;
  MacAddr da;
  MacAddr sa;
  MacAddr bssid;
  int16_t seqctl;
  unsigned char payload[];
} __attribute__((packed)) WifiMgmtHdr;

/*
 * Initialize wifi
*/
void initialize_wifi(){
  wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
  esp_wifi_init(&cfg);
  esp_wifi_set_storage(WIFI_STORAGE_RAM);
  esp_wifi_set_mode(WIFI_MODE_NULL);
}

/*
 * Starts WiFi
*/
void start_wifi(){
  esp_wifi_start();
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_promiscuous_filter(&filt);
  esp_wifi_set_promiscuous_rx_cb(&sniffer);
  esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
}

/*
 * Stops wifi
*/
void stop_wifi(){
  esp_wifi_stop();
}
/*
 * WiFi sniffer
 * This is where packets end up after they get sniffed
*/
void sniffer(void* buf, wifi_promiscuous_pkt_type_t type) { 
  wifi_promiscuous_pkt_t *p = (wifi_promiscuous_pkt_t*)buf; 
  int len = p->rx_ctrl.sig_len;
  WifiMgmtHdr *wh = (WifiMgmtHdr*)p->payload;
  
  len -= sizeof(WifiMgmtHdr);
  if (len > 0){
    //We have found a wifi device
    numWiFiDevicesFound++;
  }
}

/*
 * Scan the wifi channels for devices looking for a network
*/
bool wifi_devices_found(){
  int curChannel = 1;
  numWiFiDevicesFound = 0;
  start_wifi();
  while (curChannel <= maxCh){
    esp_wifi_set_channel(curChannel, WIFI_SECOND_CHAN_NONE);
    delay(1000);
    curChannel++;
  }
  stop_wifi();

  return numWiFiDevicesFound > 0;
  
}

//------------------------ END WiFi ------------------------//
//------------------------ START LoRa ------------------------//
//LoRa globals
#define BAND    915E6  //you can set band here directly,e.g. 868E6,915E6
unsigned int counter = 0;
String rssi = "RSSI --";
String packSize = "--";
String packet ;

/*
 * Initialize the LoRa trasmitter
*/
void initialize_LoRa(){
  Heltec.begin(true /*DisplayEnable Enable*/, true /*Heltec.Heltec.Heltec.LoRa Disable*/, true /*Serial Enable*/, true /*PABOOST Enable*/, BAND /*long BAND*/);
};

/*
 * send data over LoRa
*/
void send_data(String data){
  // send packet
  LoRa.beginPacket();
  
/*
 * LoRa.setTxPower(txPower,RFOUT_pin);
 * txPower -- 0 ~ 20
 * RFOUT_pin could be RF_PACONFIG_PASELECT_PABOOST or RF_PACONFIG_PASELECT_RFO
 *   - RF_PACONFIG_PASELECT_PABOOST -- LoRa single output via PABOOST, maximum output 20dBm
 *   - RF_PACONFIG_PASELECT_RFO     -- LoRa single output via RFO_HF / RFO_LF, maximum output 14dBm
*/
  LoRa.setTxPower(14,RF_PACONFIG_PASELECT_PABOOST);
  LoRa.print(data);
  LoRa.endPacket();
};


//------------------------ END LoRa ------------------------//
//------------------------ START Bluetooth ------------------------//

//BLE globals
int scanTime = 5; //In seconds
BLEScan* pBLEScan;

/*
 * Initialize bluetooth for scanning
*/
void initialize_bluetooth(){
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);  // less or equal setInterval value
};

/*
 * scans bluetooth and returns data
*/
bool bluetooth_devices_found(){
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  
  int devicesFound = foundDevices.getCount();
  
  pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory
  
  return devicesFound > 0;
}

//------------------------ END LoRa ------------------------//
//------------------------ START Display ------------------------//
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

//------------------------ END Display ------------------------//

/*
 * Setup the following
 *  Heltec Display - 
 *  LoRa transmitter - 
 *  BlueTooth - 
 *  Wifi - Not Done Yet
*/
void setup() {
  initialize_LoRa();
  initialize_display();
  
  print_to_display("LoRa Initialization Complete!", "Initializing Bluetooth...");
  delay(500);
  
  initialize_bluetooth();
  print_to_display("Bluetooth Initialization Complete!", "Initializing WiFi...");
  delay(500);
  
  initialize_wifi();
  print_to_display("Initializing Complete!", "You may scan when ready.");
  delay(500);
}

/*
 * Main loop
*/
void loop() {
  print_to_display("Scanning WiFi...");
  bool foundWiFiDevices = false;
  foundWiFiDevices = wifi_devices_found();

  print_to_display("WiFi scan complete!", "Scanning BLE...");
  
  bool foundBlueToothDevices = false;
  foundBlueToothDevices = bluetooth_devices_found();

  display_data(foundWiFiDevices, foundBlueToothDevices);

  String dataToSend = format_data_to_send(foundWiFiDevices, foundBlueToothDevices);
  send_data(dataToSend);
  
  delay(2000);
}


//------------------------ Helper Functions ------------------------//
/*
 * Gets the current time since last powerup as a string
*/
String get_time(){
  time_t rawtime;
  struct tm * timeinfo;

  time ( &rawtime );
  timeinfo = localtime ( &rawtime );
  return asctime (timeinfo);
}

/*
 * Format data to display and display it
*/
void display_data(bool wifiFound, bool bluetoothFound){
  String wifi_results = "No WiFi Devices...";
  String bluetooth_results = "No Bluetooth Devices...";

  if (wifiFound){
    wifi_results = "WiFi Devices Found!";
  }

  if (bluetoothFound){
    bluetooth_results = "Bluetooth Devices Found!";
  }

  String dataSent = format_data_to_send(wifiFound, bluetoothFound);
  print_to_display(wifi_results, bluetooth_results, dataSent);
}

/*
 * Format Data to send
*/
String format_data_to_send(bool wifiFound, bool bluetoothFound){
  String dataToSend;
  dataToSend += get_device_type_data(bluetoothFound, "B");
  dataToSend += get_device_type_data(wifiFound, "W");
  
  return dataToSend;
}

/*
 * Gets the data to send for a specific device type
*/
String get_device_type_data(bool foundDevice, String deviceTypeChar){
  if (foundDevice){
    return deviceTypeChar;
  }
  
  return "X";
}

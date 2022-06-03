#include <ArduinoBLE.h>

#define PERIPHERAL_ADDR "b8:27:eb:f7:1d:14"
int sensor = A0;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.println("BLE Central - Data source");
  pinMode (Sensor, INPUT); 
  // initialize the BLE hardware
  Serial.println("Initializing BLE");
  BLE.begin();
  // start scanning for peripheral
  BLE.scanForAddress(PERIPHERAL_ADDR);
}

void loop() {
  BLEDevice peripheral = BLE.available();
  if (peripheral) {
    // discovered a peripheral, print out address, local name, and advertised service
    Serial.print("Found ");
    Serial.print(peripheral.address());
    Serial.print(" '");
    Serial.print(peripheral.localName());
    Serial.print("' ");
    Serial.print(peripheral.advertisedServiceUuid());
    Serial.println();
    
    // stop scanning
    BLE.stopScan();

    // Take an analog input measurement to get data to send
    int val = analogRead(sensor);
    // Write sensor data to the data service
    writeData(val, peripheral);  

    // Delay 1 second between sensor readings
    delay(1000);
    // start scanning again
    Serial.println("Scanning for Data peripheral");
    BLE.scanForAddress(PERIPHERAL_ADDR);
  }
}

void writeData(int data, BLEDevice peripheral) {
  // connect to peripheral
  Serial.println("Connecting ...");
  if (peripheral.connect()) {
    Serial.println("Connected");
  } else {
    Serial.println("Failed to connect!");
    return;
  }
  // discover peripheral attributes
  Serial.println("Discovering attributes ...");
  if (peripheral.discoverAttributes()) {
    Serial.println("Attributes discovered");
  } else {
    Serial.println("Attribute discovery failed!");
    peripheral.disconnect();
    return;
  }
  // retrieve the Data characteristic
  BLECharacteristic dataCharacteristic = peripheral.characteristic("00000001-8cb1-44ce-9a66-001dca0941a6");
  if (!dataCharacteristic) {
    Serial.println("Peripheral does not have Data characteristic!");
    peripheral.disconnect();
    return;
  }
  // write data
  if(dataCharacteristic.canWrite()){
    dataCharacteristic.writeValue(&data, sizeof(int));
    Serial.print("Wrote Data: ");
    Serial.println(data);
  } else {
    Serial.println("Cannot write data characteristic!");
  }
  // disconnect
  if (peripheral.disconnect()) {
    Serial.println("Disconnected");
  } else {
    Serial.println("Failed to disconnect!");
    return;
  } 
}
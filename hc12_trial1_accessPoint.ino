/*    Arduino Long Range Wireless Communication using HC-12
        Example 02 - Changing channels using push buttons
   by Dejan Nedelkovski, www.HowToMechatronics.com

   Modified by David Li
*/

#include <SoftwareSerial.h>

#define setPin 6

SoftwareSerial HC12(10, 11); // HC-12 TX Pin, HC-12 RX Pin

byte incomingByte;
String readBuffer = "";

void setup() {
  Serial.begin(9600);             // Open serial port to computer
  HC12.begin(9600);               // Open serial port to HC12
  pinMode(setPin, OUTPUT);
//  digitalWrite(setPin, LOW);           // HC-12 normal, transparent mode
//  HC12.write("AT");
//  delay(100);
//  HC12.write("AT+C057");
  digitalWrite(setPin, HIGH);
}

void loop() {
  // ==== Storing the incoming data into a String variable
  while (HC12.available()) {        // If HC-12 has data
    Serial.write(HC12.read());      // Send the data to Serial monitor
  }
  delay(100);
  // ==== Sending data from one HC-12 to another via the Serial Monitor
  while (Serial.available()) {
    HC12.write(Serial.read());
  }
}


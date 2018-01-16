/*    Arduino Long Range Wireless Communication using HC-12
    Example 02 - Changing channels using push buttons - Buttons side
   by Dejan Nedelkovski, www.HowToMechatronics.com

   Modified by David Li
*/

#include <SoftwareSerial.h>

#define setPin 6
#define button1 2       // The first probe 6 in. above
#define button2 8       // The second probe 12 in. above
#define button3 12      // The third probe 18 in. above
#define button4 13      // The fourth probe 24 in. above

SoftwareSerial HC12(10, 11);         // HC-12 TX Pin, HC-12 RX Pin
byte incomingByte;
String readBuffer = "";

// The Latitude and Longitude coord will be set here
// Example: In front of EPIC
String coord;

int b1State = 0;
int b2State = 0;
int b3State = 0;
int b4State = 0;

void setup() {
  Serial.begin(9600);                   // Open serial port to computer
  HC12.begin(9600);                     // Open serial port to HC12
  coord = String("42.349992,-71.107870");
  // coord = String("1");
  pinMode(setPin, OUTPUT);
  pinMode(button1, INPUT);
  pinMode(button2, INPUT);
  pinMode(button3, INPUT);
  pinMode(button4, INPUT);
//  digitalWrite(setPin, LOW);           // HC-12 normal, transparent mode
//  HC12.write("AT");
//  delay(100);
//  HC12.write("AT+C057");
  digitalWrite(setPin, HIGH);
}

void loop() {
  while (HC12.available()) {             // If HC-12 has data
    incomingByte = HC12.read();          // Store each icoming byte from HC-12
    readBuffer += char(incomingByte);    // Add each byte to ReadBuffer string variable
  }
  delay(100);
  if(readBuffer.length() != 0) {
    HC12.print("0\n"); 
    Serial.write("HIT\n");
    delay(500);
  }
  // Check for flood presence
  b1State = digitalRead(button1);
  b2State = digitalRead(button2);
  b3State = digitalRead(button3);
  b4State = digitalRead(button4);

  // Works if "buttons" are closed simutaneously 
  if(b1State == HIGH || b2State == HIGH || b3State == HIGH || b4State == HIGH) {
    if (b4State == HIGH) {
      HC12.write("4");                   // Button 4 pressed
    } else if (b3State == HIGH) {
      HC12.write("3");                   // Button 3 pressed
    } else if (b2State == HIGH) {
      HC12.write("2");                   // Button 2 pressed
    } else if(b1State == HIGH){
      HC12.write("1");                   // Button 1 pressed
    }
    HC12.print("D" + coord);               // Send to ap that flood is present and coord
    HC12.println();
    delay(1000);
  }
  readBuffer = "";
}


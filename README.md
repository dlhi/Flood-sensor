# Flood-sensor
  This Lamppost Flood Detector project consists a flood detector unit and access point to alert user.
  The flood detector unit contains an Arduino, a HC-12 Transceiver, an antenna, a solar controller, and a solar panel. This unit measures floodwater in 6 inch increments and detects water presence by using steel conducting probes. 
  Once a probe is immersed in water, the unit will alert the access point. Each probe is preprogrammed to a specific digital pin on the Arduino. The unit sends the highest immersed probe height and the unit’s specific coordinate.
  The access point is powered by and connected to the user's computer. The Flood Detector Application should be running which is a GUI that displays the status of the flood detector unit. If a flood is detected, the GUI will sound an alarm, change its green light to red, and the data will be recorded into a text file on the user's computer. If there is no user around, the alarm will continue to sound until a user turns it off to ensure the flood has been noticed. 
  When the flood recedes, the GUI will revert back to normal. 

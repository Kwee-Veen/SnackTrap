SnackTrap is an IoT solution aimed at catching housemates who are trying to steal food from your cupboards.

It incorporates a Raspberry Pi 4 installed with a SenseHAT's light sensor and LED array.
The device employs the Blynk IoT platform to interface with sensor data and record a history of device events.
Alarm data is also sent to the Firebase cloud database in JSON format

The Blynk smartphone app can be used to monitor sensor data, and monitor or change the alarm or armed states.
The device can also be armed or disarmed using the SenseHAT's physical joystick:
- Pressing Up, Down, Up will arm the device to respond to light.
- Pressing Down, Up, Down while the device is in the alarm state (or flashing a warning prior to the alarm) will deactivate the alarm & armed states.

The device uses the SenseHAT pixel array to visually illustrate when the device is: 
- Running
- In the alarm state
- Being armed
- Being disarmed

To use the device, arm the device using either the joystick-press sequence or the Blynk smartphone app.
The device will then respond if light levels are raised above a low threshold (5/255).
While inside a dark area, such as the inside of a cupboard being monitored, the alarm will not be triggered.
If the cupboard is opened, however, the sharp increase in light will trigger the alarm and notify the user.

The device indicates an alarm state in three ways:
1) Optically, via the SenseHAT light pixel array
2) Via a Blynk smartphone app urgent notification
3) Via email sent to the Blynk project owner

The device's events, including device alarm, armed and disarmed state changes, are recorded via Blynk events.
These events are triggered by HTTP requests sent from the device to the Blynk platform upon state changes.
Reviewing the device's Timeline provides a full history of events, with alarms emphasised as Warning events.
An additional copy of JSON data highlight the time of the event is sent to Firebase, serving as a backup of events and facilitating further data processing available if desired.

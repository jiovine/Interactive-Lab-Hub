# Final Project Plan

## Team Members
Joseph Iovine (jai47)

Carlos Ponce (cmp279)

## Big idea
Create a “digital vinyl player” that uses RFID technology and spotipy to play physical albums from spotify. The device will mimic a turntable by using a servo motor. The motor will start to spin when it detects an album on top of it, and the RFID scanner will read the album and start to play it from spotify.
![Final Project Sketch](iddfinal.jpeg)

## Timeline
1. Order additional parts - within the next week
2. Get spotify API working with the Rpi
3. Just be able to play audio out of the Rpi from my spotify account
4. Get RFID scanner working with the Rpi - just be able to recognize tags and perform an action when recognized
5. Get RFID scanner working with spotipy
6. Be able to copy spotify URI’s onto the tags and when scanned it starts to play that specific album from the Rpi
7. Get RFID scanner working with servo motor
8. Recognize tag and prompt the servo motor to start spinning, and when tag is removed it will stop spinning
9. Build the physical device - will look like a mini turntable with servo motor, RFID scanner and Rpi inside
10. Test it with users!


## Parts needed
* RFID scanner
* RFID tags
* Continous Servo motor


## Risks/contingencies
The servo motor only rotates 90 degrees, need to hack it to make it a continuous rotation device
Playing audio directly from the Rpi seems a little difficult, doesn’t work through bluetooth or hdmi


## Fall-back plan
If the Rpi cannot play music directly, we will utilize spotify connect to remotely play through another device that is connected to a bluetooth speaker. In addition, if the servo motor cannot turn continuously we will just wizard that portion for the demo.
A look based media player that pauses itself when user is not looking at it and resumes as soon as the user looks at it again.
This is done using the camera or webcam on top of the computer. As long as the camera detects the users face looking at it, the media is played. The player pauses as soon as users face is not completely seen. When the user also is sleepy it pauses giving an alarm. 

---
## Algorithm
- The Media Player is created using pyqt5
- The face detection is done using opencv cascade classifier
- The eye blinking and drowiness is done using  dlib’s pre-trained facial landmark detector.

---
## Functionality

![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Media_Player/Capture.PNG?raw=true)

 1. Click on openfile and choose the file you want to play
 2. Press play button
 3. To start the face,sleepiness-detection you click on face detection button, then the webcam will start capturing the face & the eyes
 
 > Note: While face detection is on, you can manually pause by clicking on ESC to close the face detection first, then click on the pause button
 
---

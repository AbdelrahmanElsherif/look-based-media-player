A look based media player that pauses automatically when user is not looking at it and resumes as soon as the user looks at it again.
This is done using the camera or webcam on top of the computer. As long as the camera detects the users face looking at it, the media is played. The player pauses as soon as users face is not completely seen. When the user also is sleepy it pauses the video playing and gives a warning message to the user. 

---
## Algorithm
- The Media Player is created using PyQt5
- Face Detection is done using opencv cascade classifier
- Eye blinking and drowiness is done using  dlib’s pre-trained facial landmark detector.

---
## Installation 
- Download lastest most compatible python version to your OS https://www.python.org/downloads/ 
- Python 3.6 and 3.7 were used in developing the project
```
python -m pip install -r requirements.txt
```

## Functionality

![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Media_Player/Capture.PNG?raw=true)

 1. Click on openfile and choose the file you want to play
 2. Press play button
 3. To start the face,sleepiness-detection you click on face detection button, then the webcam will start capturing the face & the eyes
 
 > Note: While face detection is on, you can manually pause by clicking on ESC to close the face detection first, then click on the pause button
 
---

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

Media Player GUI
![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Media_Player/Screenshot%20(178).png?raw=true)

Click on Open Video and choose the file you want to play then press the Play button 
![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Media_Player/Screenshot%20(179).png?raw=true)

Press Face Detection button to enable Face Detection and Drowsiness feature 
Webcam feed window will be shown 

On entering a wrong file format or no file at all, file error window will pop up 
![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Media_Player/Screenshot%20(181).png?raw=true)

Pressing Retry button, will enable the user to choose another file 
Pressing Abort button, will close and the mediaplayer 


On detecting eyes dowsiness and sleepliness, Drowsiness window will pop up 
![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Media_Player/Screenshot%20(182).png?raw=true)
Pressing Retry button, will enable the user to contiue watching 
Pressing Abort button, will close and exit the medialayer  



 
 > Note: While face detection is on, you can manually pause by clicking on ESC to close the face detection first, then click on the pause button
 
---

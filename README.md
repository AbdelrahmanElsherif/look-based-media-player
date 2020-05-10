# Look-Based MediaPlayer 
A look based media player that pauses automatically when user is not looking at it and resumes as soon as the user looks at it again.
This is done using the camera or webcam on top of the computer. As long as the camera detects the users face looking at it, the media is played. The player pauses as soon as users face is not completely seen. When the user also is sleepy it pauses the video playing and gives a warning message to the user. 



---
## Presentation Demo 

## Algorithm
- The Media Player is created using PyQt5
- Face Detection is done using opencv cascade classifier
- Eye blinking and drowiness is done using  dlib’s pre-trained facial landmark detector.

---
## Installation 
- Download lastest most compatible python version to your OS --> [Click Here](https://www.python.org/downloads/?c=hpgsf9 )
- Python 3.6 and 3.7 were used in developing the project
```
python -m pip install -r requirements.txt
```

## Functionality

- Media Player GUI <br />
![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/tree/master/Screenshots/Screenshot%20(187).png?raw=true)
 <br />
 <br />
 
- Click on Open Video and choose the file you want to play then press the Play button <br />
![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/tree/master/Screenshotsr/Screenshot%20(179).png?raw=true)
 <br />
 <br />
 
- Press Face Detection button to enable Face Detection and Drowsiness feature <br />
  Webcam feed window will be shown <br />
  
  HAN7OOT SORET EL WEBCAM FEED HENA 
  
   > Note: To regain manual control over mediaplayer, Press ESC to release webcam feed <br />
   You can return back to face detection feature by pressing face detection button <br />
   >>At first video will paused because user's face is not detected it 

 <br />
 <br />
 
 - On entering a wrong file format or no file at all, file error window will pop up <br />
 ![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/tree/master/Screenshots/Screenshot%20(181).png?raw=true)

   >Pressing Retry button, will enable the user to choose another file <br />
   Pressing Abort button, will close and the mediaplayer 

 <br />
  <br />
  
 - On detecting eyes dowsiness and sleepliness, Drowsiness window will pop up <br />
 ![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/tree/master/Screenshots/Screenshot%20(182).png?raw=true)

   >Pressing Retry button, will enable the user to contiue watching <br />
   Pressing Abort button, will close and exit the medialayer <br />
    >>Note: On pressing Retry user's eyes should be wide open to continue playing the video otherwise it might take a couple of times   pressing Retry button 
    

 ## Supported Formats 

 - .mp3 
 - .mp4 
 - .mov 
 - .mkv 
 - .wav 

 
---

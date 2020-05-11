# Look-Based MediaPlayer 
A look based media player that pauses automatically when user is not looking or paying attention and resumes as soon as the user is looking at it or his attention to the video is restored.  <br />
This is done using the camera or webcam on top of the computer. As long as the camera detects the users face looking at it, the media is playing. The video pauses as soon as users face is not completely seen.  <br />
When the user is sleepy for more than 48 secs, it pauses the video playing and gives a warning message to the user. 



---
## Overview Demo
 ![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Screenshots/ezgif.com-crop.gif?raw=true)  <br />
**For Detailed video** [Click Here](https://youtu.be/k3kdQFkdYWA)

## Algorithm
- The Media Player is created using PyQt5
- Face Detection is done using opencv cascade classifier
- Eye blinking and drowiness is done using  dlib’s pre-trained facial landmark detector.

---
## Installation 
- Download lastest most compatible python version to your OS [Click Here](https://www.python.org/downloads/?c=hpgsf9 )
> Note: Python 3.6 and 3.7 were used in developing the project
- Clone the repo or Download it as zip 
- Put everything into a single folder  
- Open cmd in project folder **Look Based Media Player** and run this command 
```
python -m pip install -r requirements.txt
```

## Usage 

 - Go to  **Look Based Media Player** 
 - Open **output\LookAlive** folder and search for **LookAlive.exe** 
 - Run and Experiment the Desktop app 
      #### OR     
 - Open **Look Alive.py** and run it 

## Functionality

- Media Player GUI <br />
![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Screenshots/Screenshot%20(187).png?raw=true)
 <br />
 <br />
 
- Click on Open Video and choose the file you want to play then press the Play button <br />
![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Screenshots/Screenshot%20(179).png?raw=true)
 <br />
 <br />
 
- Press Face Detection button to enable Face Detection and Drowsiness feature <br />
  Webcam feed window will be shown <br />
  
 ![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Screenshots/Screenshot%20(191).png?raw=true)
  
 
   > Note: To regain manual control over mediaplayer, Press ESC to release webcam feed <br />
   You can return back to face detection feature by pressing face detection button <br />
   >>At first video might pause because user's face is not detected yet

 <br />
 <br />
 
 - On entering a wrong file format or no file at all, file error window will pop up <br />
 ![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Screenshots/Screenshot%20(181).png?raw=true)

   >Pressing Retry button, will enable the user to choose another file <br />
   Pressing Abort button, will close open file window  

 <br />
  <br />
  
 - On detecting eyes dowsiness and sleepliness, Drowsiness window will pop up <br />
 ![alt text](https://github.com/AbdelrahmanElsherif/look-based-media-player/blob/master/Screenshots/Screenshot%20(182).png?raw=true)

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

from __future__ import print_function
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import *
import sys
import cv2 as cv
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib

global ALARM_ON
global ear


# The function used in Face Detection to compute the ear,
# through computing the ratio of distances between
# the vertical eye landmarks and the distances between the horizontal eye landmarks

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


class Window (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Look Alive")
        self.setGeometry(350,100,700,500)
        self.setWindowIcon(QIcon('Player.png'))
        self.mainMenu = QMenuBar()
        self.setStyleSheet("""
               QMenuBar {
                   background-color: rgb(49,49,49);
                   color: rgb(255,255,255);
                   border: 1px solid #000;
               }

               QMenuBar::item {
                   background-color: rgb(49,49,49);
                   color: rgb(255,255,255);
               }

               QMenuBar::item::selected {
                   background-color: rgb(30,30,30);
               }

               QMenu {
                   background-color: rgb(49,49,49);
                   color: rgb(255,255,255);
                   border: 1px solid #000;           
               }

               QMenu::item::selected {
                   background-color: rgb(30,30,30);
               }
           """)
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(QAction("Open Video", self))
        self.fileMenu.addAction(QAction("Exit", self))
        self.fileMenu.addAction(QAction("Help ", self))
        p = self.palette()
        p.setColor(QPalette.Window,Qt.white)
        self.setPalette(p)
        self.init_ui()
        self.show()

    # To Create the widgets we need
    def init_ui(self):

        # Create a Media player object
        self.mediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Create Video widget object
        videowidget = QVideoWidget()

        # Face detection and drowsiness button
        faceDetetction = QPushButton("Face Detection")
        faceDetetction.setStyleSheet("color: white; font-size: 16px; background-color: #2b5b84;" "border-radius: 10px; padding: 10px; text-align: center; ")
        faceDetetction.clicked.connect(self.FaceDetection)

        # Create Open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)
        openBtn.setStyleSheet("QPushButton::pressed""{""background-color : white;""}")
        openBtn.setStyleSheet("color: white; font-size: 12px; background-color: #2b5b84; border-radius: 10px;"" padding: 10px; text-align: center;")

        # Create an Information Label
        self.label2 =QLabel()
        self.label2.setStyleSheet("color:#2b5b84 ; font-size: 12px; border-radius: 10px; padding:"" 10px; text-align: center;")
        self.label2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.label2.setText("To Exit Face Detection Press ESC")

        # Create Play button
        self.playBtn=QPushButton()
        self.playBtn.setIcon(QIcon("blueplay.jpg"))
        self.playBtn.clicked.connect(self.play_video)
        self.playBtn.setStyleSheet("color: black; font-size: 12px; background-color: #FF8C00;"" border-radius: 10px; padding: 10px; text-align: center;")
        self.playBtn.setStyleSheet("QPushButton::pressed" "{" "background-color : green;""}")

        # Create Stop button
        self.stopBtn = QPushButton()
        self.stopBtn.setIcon(QIcon("bluestop.jpg"))
        self.stopBtn.setStyleSheet("QPushButton::pressed""{" "background-color : red;""}" )
        self.stopBtn.pressed.connect(self.stop_video)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create Position slider
        self.slider=QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Create volume label image
        self.label1=QLabel()
        self.label1.setText("")
        self.label1.setPixmap(QPixmap("speaker-volume"))

        # Create volume slider
        self.volumeSlider = QSlider()
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.volumeSlider.valueChanged.connect(self.mediaplayer.setVolume)

        #Adding a spacer item in the Hbox
        spacer =QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Create Hbox Layout
        hboxlayout= QHBoxLayout()
        hboxlayout.setContentsMargins(0, 0, 0, 0)

        # Set Widgets to the hbox layout
        hboxlayout.addWidget(openBtn)
        hboxlayout.addWidget(self.playBtn)
        hboxlayout.addWidget(self.stopBtn)
        hboxlayout.addItem(spacer)
        hboxlayout.addWidget(self.label1)
        hboxlayout.addWidget(self.volumeSlider)


        # Create vbox layout ( will be the main layout including the hbox layout)
        vboxlayout=QVBoxLayout()
        vboxlayout.addWidget(videowidget)
        vboxlayout.addWidget(self.slider)
        vboxlayout.addLayout(hboxlayout)
        vboxlayout.addWidget(self.label2)
        vboxlayout.addWidget(faceDetetction)

        # Set the layout to your window
        self.setLayout((vboxlayout))

        # Get the video to output on the video widget window
        self.mediaplayer.setVideoOutput(videowidget)

        # Media player signals
        self.mediaplayer.stateChanged.connect(self.mediastate_changed)
        self.mediaplayer.positionChanged.connect(self.position_changed)
        self.mediaplayer.durationChanged.connect(self.duration_changed)

    # Choosing media file from your device
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "mp3 Audio (*.mp3);mp4 Video (*.mp4);"
                                                                         "Movie files (*.mov);All files (*.*)")

        if filename != '':
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
        # Error handling in case wrong format media file is choosen
        if not filename.endswith('.mp3') | filename.endswith('.mp4') | filename.endswith('.mov') | filename.endswith('.mkv')\
                | filename.endswith('.MP3') | filename.endswith('.MP4') | filename.endswith('.MOV') | filename.endswith('.MKV')\
                | filename.endswith('.wav') | filename.endswith('.WAV'):

          # Create warning message box and it characteristics
            msg1 = QMessageBox()
            msg1.setWindowTitle("File Error !")
            msg1.setText("Invalid File Type")
            msg1.setIcon(QMessageBox.Warning)
            msg1.setWindowIcon(QIcon('file error.png'))
            msg1.setStandardButtons(QMessageBox.Retry | QMessageBox.Abort)
            msg1.setStyleSheet('QMessageBox {background-color: #2b5b84; color: white;}\n QMessageBox {color: white;}\n ''QPushButton{color: white; font-size: 16px; background-color: #1d1d1d; '  'border-radius: 10px; padding: 10px; text-align: center;}\n QPushButton:hover{color: #2b5b84;}')
            msg1.buttonClicked.connect(self.popup1)
            y = msg1.exec_()

    # pop up message if the user choose an invalid input type
    def popup1(self, i):
        # if the user choose retry he can can try again to choose a file of a valid format
        if i.text() == 'Retry':
            self.open_file()
        # if the user chooses to abort then the window is closed
        if i.text() == 'Abort':
            cv.destroyAllWindows()


    # Stoping the video and replay it agaian from the beginning
    def stop_video(self):
        self.mediaplayer.stop()
        self.playBtn.setIcon(QIcon('blueplay.jpg'))

    # Pressing play button while it's in pause state, Plays the video
    #Pressing play button while it's in play state , Pauses the video
    def play_video(self):
        if self.mediaplayer.state()  == QMediaPlayer.PlayingState:
            self.mediaplayer.pause()
            self.playBtn.setIcon(QIcon('blueplay.jpg'))
        else:
            self.mediaplayer.play()
            self.playBtn.setIcon(QIcon('bluepause.jpg'))

    # Linking mediaplayer state to play button
    def mediastate_changed(self, state):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(QIcon('blueplay.jpg'))
        else:
            self.playBtn.setIcon(QIcon('bluepause.jpg'))

    # Changing slider position while video is playing
    def position_changed(self, position):
        self.slider.setValue(position)

    # Changing slider duration range ehike the video is playing
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaplayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaplayer.errorString())


    # On clicking face detetction button this method is executed
    def FaceDetection(self):

        # Threshold ratio to indicate a blink
        EYE_AR_THRESH = 0.2
        # Number of frames threshold above which video is paused
        EYE_AR_CONSEC_FRAMES = 30

        # Initialize the frame counter as well as a boolean used to
        # indicate if the alarm is going off
        COUNTER = 0
        ALARM_ON = False

        # Initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        # Grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        # Open the webcam and read the stream
        cap = cv.VideoCapture(0)
        # Use opencv cascade classifier in detecting the face
        face_cascade = cv.CascadeClassifier("haarcascade_frontalface_alt.xml")

        while True:
            # get the frames from the webcam
            ret, frame = cap.read()
            # convert the frames from rgb into grey
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame_gray = cv.equalizeHist(frame_gray)
            # use the detector and get the rectangles from it
            rects = detector(frame_gray, 0)

            # -- Detect faces
            faces = face_cascade.detectMultiScale(frame_gray, minSize=(85, 85))
            # count the number of face in front of the cam
            how_many_faces = len(faces)

            for (x, y, w, h) in faces:
                # detect the center of the face
                center = (x + w // 2, y + h // 2)
                # draw an ellipse on the face
                frame = cv.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
                faceROI = frame_gray[y:y + h, x:x + w]

            for rect in rects:
                # determine the facial landmarks for the face
                shape = predictor(frame_gray, rect)
                # convert the facial landmark from (x, y) coordinates to a numpy array
                shape = face_utils.shape_to_np(shape)
                # extract the left and right eye coordinates
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                # use the coordinates to compute the eye aspect ratio for both eyes
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)

                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0

                # compute the convex hull for the left and right eye
                leftEyeHull = cv.convexHull(leftEye)
                rightEyeHull = cv.convexHull(rightEye)
                # draw contours around eyes
                cv.drawContours(frame, [leftEyeHull], -1, (75, 50, 130), 1)
                cv.drawContours(frame, [rightEyeHull], -1, (75, 50, 130), 1)

                # check if the eye aspect ratio is below the threshold, if so increment the counter of frames
                if ear < EYE_AR_THRESH:
                    COUNTER += 1

                    # if the eyes were closed for more than the number of frames threshold (30) then put the alarm on
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        # if the alarm is not on, turn it on
                        if not ALARM_ON:
                            ALARM_ON = True

                        # draw an alarm on the frame
                        cv.putText(frame, "Sleepy Eyes Detected", (10, 30),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                # if the ear is greater than the threshold then reset the counter of frames
                else:
                    COUNTER = 0
                    ALARM_ON = False

                # put the value of ear detected
                cv.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                           cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            # visualize the camera frame
            cv.imshow('YOU ARE BEING WATCHED ', frame)

            # if no faces are detected then pause
            if how_many_faces == 0:
                self.mediaplayer.pause()
                self.mediaplayer.stateChanged
                self.playBtn.setIcon(QIcon('blueplay.jpg'))
                self.mediaplayer.positionChanged.connect(self.position_changed)
                self.mediaplayer.durationChanged.connect(self.duration_changed)

            # if the alarm is on which means the ear is less than the threshold for 30 frames then pause
            elif ALARM_ON:
                self.mediaplayer.pause()
                self.mediaplayer.stateChanged
                self.playBtn.setIcon(QIcon('blueplay.jpg'))
                self.mediaplayer.positionChanged.connect(self.position_changed)
                self.mediaplayer.durationChanged.connect(self.duration_changed)


                # alert that the user is sleepy and must choose to either continue watching or abort&close the player
                msg = QMessageBox()
                msg.setWindowTitle("Drowsiness ")
                msg.setText("You're getting sleepy would you like to ")
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowIcon(QIcon('sleepy1.png'))
                msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Abort)
                msg.setStyleSheet('QMessageBox {background-color: #2b5b84; color: white;}\n'
                                  ' QMessageBox {color: white;}\n ''QPushButton{color: white; font-size: 16px;'
                                  'background-color: #1d1d1d;''border-radius: 10px; padding: 10px;'
                                  ' text-align: center;}\n QPushButton:hover{color: #2b5b84;}')
                msg.buttonClicked.connect(self.popup)
                x= msg.exec_()

            # if not sleepy or the face is detected then continue playing
            else:
                self.mediaplayer.play()
                self.mediaplayer.stateChanged
                self.playBtn.setIcon(QIcon('bluepause.jpg'))

            # if ESC button is hit, then the camera frame is closed and the user is back to manual control
            if cv.waitKey(10) == 27:
                cap.release()
                cv.destroyWindow('YOU ARE BEING WATCHED ')
                break

    # Warning Message box that pops up if the user is sleepy
    def popup(self, i):

        # if the user choose to Retry, then the media player is resumed and the ear is back to normal
        # and the alarm if now off
        if i.text() == "Retry":
            ear = 0.31
            ALARM_ON = False
            self.mediaplayer.play()
            self.mediaplayer.stateChanged
            self.playBtn.setIcon(QIcon('bluepause.jpg'))

        # if the user chooses to abort then the media player is closed and the user can sleep
        if i.text() == "Abort":
            sys.exit(app.exec_())

# Initiate the application
app = QApplication(sys.argv)
app.setStyle("Fusion")
# Make an instance of the Window class
window = Window()
sys.exit(app.exec_())
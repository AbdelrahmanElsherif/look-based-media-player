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
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib

global ALARM_ON
global ear

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
        p = self.palette()
        p.setColor(QPalette.Window,Qt.white)
        self.setPalette(p)
        self.init_ui()
        self.show()

    #To Create the widgets we need
    def init_ui(self):

        #Create a Media player object
        self.mediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #Create Video widget object
        videowidget = QVideoWidget()
        faceDetetction = QPushButton("Face Detection")
        faceDetetction.setStyleSheet("color: white; font-size: 16px; background-color: #2b5b84; border-radius: 10px; padding: 10px; text-align: center; ")
        faceDetetction.clicked.connect(self.FaceDetection)

        #Create Open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)
        openBtn.setStyleSheet("QPushButton::pressed"
                                   "{"
                                   "background-color : white;"
                                   "}"
                                   )
        openBtn.setStyleSheet("color: white; font-size: 12px; background-color: #2b5b84; border-radius: 10px; padding: 10px; text-align: center;")

        self.label2 =QLabel()
        self.label2.setStyleSheet("color:#2b5b84 ; font-size: 12px; border-radius: 10px; padding: 10px; text-align: center;")
        self.label2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.label2.setText("To Exit Face Detection Press ESC")

        #Create Play button
        self.playBtn=QPushButton()
        #self.playBtn .setEnabled(False)
        self.playBtn.setIcon(QIcon("blueplay.jpg"))
       # self.playBtn.setStyleSheet("background-color: yellow ")
        #self.playBtn.setIcon (self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        self.playBtn.setStyleSheet(
            "color: black; font-size: 12px; background-color: #FF8C00; border-radius: 10px; padding: 10px; text-align: center;")
        self.playBtn.setStyleSheet("QPushButton::pressed"
                                   "{"
                                   "background-color : green;"
                                   "}"
                                   )


        #Create Stop button
        self.stopBtn = QPushButton()
        self.stopBtn.setIcon(QIcon("bluestop.jpg"))
        self.stopBtn.setStyleSheet("QPushButton::pressed"
                                   "{"
                                   "background-color : red;"
                                   "}"
                                   )
        self.stopBtn.pressed.connect(self.mediaplayer.stop)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)


        #Create slider
        self.slider=QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)


        #create volume label image
        self.label1=QLabel()
        self.label1.setText("")
        self.label1.setPixmap(QPixmap("speaker-volume"))
        #self.label1.setFixedSize(100,100)

        #create volume slider
        self.volumeSlider = QSlider()
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.volumeSlider.valueChanged.connect(self.mediaplayer.setVolume)


        spacer =QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        #Create Hbox Layout
        hboxlayout= QHBoxLayout()
        hboxlayout.setContentsMargins(0, 0, 0, 0)

        #Set Widgets to the hbox layout
        hboxlayout.addWidget(openBtn)
        hboxlayout.addWidget(self.playBtn)
        hboxlayout.addWidget(self.stopBtn)
        hboxlayout.addItem(spacer)
        hboxlayout.addWidget(self.label1)
        hboxlayout.addWidget(self.volumeSlider)


        #hboxlayout.addItem(spacerItem)

        #Create another hbox
        hboxlayout1 = QHBoxLayout()
        hboxlayout1.setContentsMargins(0, 0, 0, 0)

        #Set its widgets
        self.currentTimeLabel = QLabel()
        self.currentTimeLabel.setMinimumSize(QSize(80, 0))
        self.currentTimeLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing )
        self.currentTimeLabel.setObjectName("currentTimeLabel")
        self.totalTimeLabel = QLabel()
        self.totalTimeLabel.setMinimumSize(QSize(80, 0))
        self.totalTimeLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft )
        self.totalTimeLabel.setObjectName("totalTimeLabel")
        self.currentTimeLabel.setText("0:00")
        self.totalTimeLabel.setText( "0:00")
       # hboxlayout1.addWidget(self.currentTimeLabel)
        #hboxlayout1.addWidget(self.slider)
       # hboxlayout1.addWidget(self.totalTimeLabel)





        #create vbox layout ( will be the main layout including the hbox layout)
        vboxlayout=QVBoxLayout()
        vboxlayout.addWidget(videowidget)
        vboxlayout.addWidget(self.slider)
        vboxlayout.addLayout(hboxlayout)
        vboxlayout.addWidget(self.label2)
        vboxlayout.addWidget(faceDetetction)

        # set the layout to your window
        self.setLayout((vboxlayout))
        # get the video to output on the window
        self.mediaplayer.setVideoOutput(videowidget)

        # media player signals

        self.mediaplayer.stateChanged.connect(self.mediastate_changed)
        self.mediaplayer.positionChanged.connect(self.position_changed)
        self.mediaplayer.durationChanged.connect(self.duration_changed)

    # To choose file from Pc method & enabling the play button
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "mp3 Audio (*.mp3);mp4 Video (*.mp4);Movie files (*.mov);All files (*.*)")

        if filename!= '':
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
           # print(filename)

        if not filename.endswith('.mp3')|filename.endswith('.mp4')|filename.endswith('.mov')|filename.endswith('.mp3')|filename.endswith('.mkv'):
            msg1 = QMessageBox()
            msg1.setWindowTitle("File Error ")
            msg1.setText("Invalid File Type ")
            msg1.setIcon(QMessageBox.Warning)
            msg1.setWindowIcon(QIcon('file error.png'))
            msg1.setStandardButtons(QMessageBox.Retry | QMessageBox.Abort)
            msg1.setStyleSheet(
                'QMessageBox {background-color: #2b5b84; color: white;}\n QMessageBox {color: white;}\n QPushButton{color: white; font-size: 16px; background-color: #1d1d1d; border-radius: 10px; padding: 10px; text-align: center;}\n QPushButton:hover{color: #2b5b84;}')
            msg1.buttonClicked.connect(self.popup1)
            y = msg1.exec_()


    def popup1(self,i):
        if i.text()=='Retry':
            filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                      "mp3 Audio (*.mp3);mp4 Video (*.mp4);Movie files (*.mov);All files (*.*)")

            if filename != '':
                self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
                self.playBtn.setEnabled(True)
            # print(filename)

        else:
            cv.destroyAllWindows()


    # If the video is paused clicking play button enables it, else if it's playing clicking play button pauses it
    def play_video(self):
        if self.mediaplayer.state()  == QMediaPlayer.PlayingState:
            self.mediaplayer.pause()
            self.playBtn.setIcon(QIcon('bluepause.jpg'))
            print("Paused")

        else:
            self.mediaplayer.play()
            self.playBtn.setIcon(QIcon('blueplay.jpg'))
            print("played")


    def mediastate_changed(self, state):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(QIcon('bluepause.jpg'))


        else:
            self.playBtn.setIcon(QIcon('blueplay.jpg'))



    def position_changed(self, position):
        self.slider.setValue(position)


    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaplayer.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaplayer.errorString())



    def FaceDetection(self):

        # define two constants, one for the eye aspect ratio to indicate
        # blink and then a second constant for the number of consecutive
        # frames the eye must be below the threshold for to set off the
        # alarm

        EYE_AR_THRESH = 0.3
        EYE_AR_CONSEC_FRAMES = 48

        # initialize the frame counter as well as a boolean used to
        # indicate if the alarm is going off
        COUNTER = 0
        ALARM_ON = False

        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        print("[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        # grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        # -- 2. Read the video stream
        cap = cv.VideoCapture(0)
        face_cascade = cv.CascadeClassifier("haarcascade_frontalface_alt.xml")

        while True:
            ret, frame = cap.read()
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame_gray = cv.equalizeHist(frame_gray)
            rects = detector(frame_gray, 0)

            # -- Detect faces
            faces = face_cascade.detectMultiScale(frame_gray, minSize=(85, 85))
            how_many_faces = len(faces)
            print(how_many_faces)
            for (x, y, w, h) in faces:
                center = (x + w // 2, y + h // 2)
                frame = cv.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
                faceROI = frame_gray[y:y + h, x:x + w]

            for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(frame_gray, rect)
                shape = face_utils.shape_to_np(shape)
                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)

                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0

                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv.convexHull(leftEye)
                rightEyeHull = cv.convexHull(rightEye)
                cv.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

                # check to see if the eye aspect ratio is below the blink
                # threshold, and if so, increment the blink frame counter
                if ear < EYE_AR_THRESH:
                    COUNTER += 1

                    # if the eyes were closed for a sufficient number of
                    # then sound the alarm
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        # if the alarm is not on, turn it on
                        if not ALARM_ON:
                            ALARM_ON = True

                        # draw an alarm on the frame
                        cv.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # otherwise, the eye aspect ratio is not below the blink
                # threshold, so reset the counter and alarm
                else:
                    COUNTER = 0
                    ALARM_ON = False

                # draw the computed eye aspect ratio on the frame to help
                # with debugging and setting the correct eye aspect ratio
                # thresholds and frame counters
                cv.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                           cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)



            cv.imshow('YOU ARE BEING WATCHED ', frame)
            if how_many_faces == 0:
                manual = 0
                self.mediaplayer.pause()
                self.mediaplayer.stateChanged
                self.playBtn.setIcon(QIcon('bluepause.jpg'))
                #self.mediaplayer.stateChanged.connect(self.mediastate_changed)
                self.mediaplayer.positionChanged.connect(self.position_changed)
                self.mediaplayer.durationChanged.connect(self.duration_changed)
            elif ALARM_ON == True :
                manual = 0
                self.mediaplayer.pause()
                self.mediaplayer.stateChanged
                self.playBtn.setIcon(QIcon('bluepause.jpg'))
                # self.mediaplayer.stateChanged.connect(self.mediastate_changed)
                self.mediaplayer.positionChanged.connect(self.position_changed)
                self.mediaplayer.durationChanged.connect(self.duration_changed)
              #  error_dialog = QErrorMessage()
              #  error_dialog.showMessage("You're getting Sleepy")
             #   error_dialog.set
                msg = QMessageBox()
                msg.setWindowTitle("Drowsiness ")
                msg.setText("You're getting sleepy would you like to ")
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowIcon(QIcon('sleepy1.png'))
                msg.setStandardButtons( QMessageBox.Retry| QMessageBox.Abort )
                msg.setStyleSheet(
                    'QMessageBox {background-color: #2b5b84; color: white;}\n QMessageBox {color: white;}\n QPushButton{color: white; font-size: 16px; background-color: #1d1d1d; border-radius: 10px; padding: 10px; text-align: center;}\n QPushButton:hover{color: #2b5b84;}')
                msg.buttonClicked.connect(self.popup)
                x= msg.exec_()
            else:
                self.mediaplayer.play()
                self.mediaplayer.stateChanged
                self.playBtn.setIcon(QIcon('blueplay.jpg'))

            if cv.waitKey(10) == 27:
                cap.release()
                # sys.exit()
                # cv2.destroyAllWindows()
                break

    def popup(self,i):
        print(i.text())
        if i.text() == "Retry":
            ear = 0.31
            ALARM_ON = False
            self.mediaplayer.play()
            self.mediaplayer.stateChanged
            self.playBtn.setIcon(QIcon('blueplay.jpg'))

        if i.text() == "Abort":
            cv.detrotyAllWindows()




#Initiate the application
app=QApplication(sys.argv)
app.setStyle("Fusion")
#Make an instance of the Window class
window=Window()
sys.exit(app.exec_())
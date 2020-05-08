from __future__ import print_function
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import *
import sys
import cv2 as cv




class Window (QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Look Alive")
        self.setGeometry(350,100,700,500)
        self.setWindowIcon(QIcon('Player.png'))

        p = self.palette()
        p.setColor(QPalette.Window,Qt.black)
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
        faceDetetction.setStyleSheet("background-color: orange ")
        faceDetetction.clicked.connect(self.FaceDetection)

        #Create Open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)
        openBtn.setStyleSheet("QPushButton::pressed"
                                   "{"
                                   "background-color : black;"
                                   "}"
                                   )
        openBtn.setStyleSheet("background-color: orange")

        self.label2 =QLabel()
        self.label2.setStyleSheet("color: orange;")
        self.label2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.label2.setText("To Exit Face Detection Press ESC")

        #Create Play button
        self.playBtn=QPushButton()
        #self.playBtn .setEnabled(False)
        self.playBtn.setIcon(QIcon("play1.png"))
        self.playBtn.setStyleSheet("background-color: yellow ")
        #self.playBtn.setIcon (self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        self.playBtn.setStyleSheet("QPushButton::pressed"
                                   "{"
                                   "background-color : green;"
                                   "}"
                                   )

        #Create Stop button
        self.stopBtn = QPushButton()
        self.stopBtn.setIcon(QIcon("stop1.png"))
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



    # If the video is paused clicking play button enables it, else if it's playing clicking play button pauses it
    def play_video(self):
        if self.mediaplayer.state()  == QMediaPlayer.PlayingState:
            self.mediaplayer.pause()
            self.playBtn.setIcon(QIcon('pause1.png'))
            print("Paused")

        else:
            self.mediaplayer.play()
            self.playBtn.setIcon(QIcon('play1.png'))
            print("played")




    def FaceDetection(self):

        # -- 2. Read the video stream
        cap = cv.VideoCapture(0)
        face_cascade = cv.CascadeClassifier("haarcascade_frontalface_alt.xml")
        eyes_cascade = cv.CascadeClassifier("haarcascade_eye.xml")
        while True:
            ret, frame = cap.read()
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame_gray = cv.equalizeHist(frame_gray)

            # -- Detect faces
            faces = face_cascade.detectMultiScale(frame_gray, minSize=(85, 85))
            how_many_faces = len(faces)
            for (x, y, w, h) in faces:
                center = (x + w // 2, y + h // 2)
                frame = cv.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
                faceROI = frame_gray[y:y + h, x:x + w]
                # print(x ,y , x, h)

                eyes = eyes_cascade.detectMultiScale(faceROI)
                for (x2, y2, w2, h2) in eyes:
                    eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
                    radius = int(round((w2 + h2) * 0.25))
                    frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)
            cv.imshow('YOU ARE BEING WATCHED ', frame)
            if how_many_faces == 0:
                manual = 0
                self.mediaplayer.pause()
                self.mediaplayer.stateChanged
                self.playBtn.setIcon(QIcon('pause1.png'))
                #self.mediaplayer.stateChanged.connect(self.mediastate_changed)
                self.mediaplayer.positionChanged.connect(self.position_changed)
                self.mediaplayer.durationChanged.connect(self.duration_changed)
            else:

                self.mediaplayer.play()
                self.mediaplayer.stateChanged
                self.playBtn.setIcon(QIcon('play1.png'))

            if cv.waitKey(10) == 27:
                cap.release()
                # sys.exit()
                # cv2.destroyAllWindows()
                break


    def mediastate_changed(self, state):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(QIcon('pause1.png'))


        else:
            self.playBtn.setIcon(QIcon('play1.png'))



    def position_changed(self, position):
        self.slider.setValue(position)


    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaplayer.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaplayer.errorString())









#Initiate the application
app=QApplication(sys.argv)
app.setStyle("Fusion")
#Make an instance of the Window class
window=Window()
sys.exit(app.exec_())


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle,\
    QSizePolicy, QFileDialog
import sys
from PyQt5.QtGui import  QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl


class Window (QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Media Player")
        self.setGeometry(350,100,700,500)
        self.setWindowIcon(QIcon('playericon.png'))

        p = self.palette()
        p.setColor(QPalette.Window,Qt.black)
        self.setPalette(p)

        self.init_ui()


        self.show()

    #To create the widgets we need
    def init_ui(self):

        #Create a media player object
        self.mediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #Create video widget object
        videowidget = QVideoWidget()

        #Create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)

        #Create button for playing
        self.playBtn=QPushButton()
        self.playBtn .setEnabled(False)
        self.playBtn.setIcon (self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        #Create slider
        self.slider=QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)


        #create label

        self.label=QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Maximum)


        #Create Hbox Layout
        hboxlayout= QHBoxLayout()
        hboxlayout.setContentsMargins(0, 0, 0, 0)

        #Set Widgets to the hbox layout
        hboxlayout.addWidget(openBtn)
        hboxlayout.addWidget(self.playBtn)
        hboxlayout.addWidget(self.slider)


        #create vbox layout ( will be the main layout including the hbox layout)
        vboxlayout=QVBoxLayout()
        vboxlayout.addWidget(videowidget)
        vboxlayout.addLayout(hboxlayout)
        vboxlayout.addWidget(self.label)

        # set the layout to your window
        self.setLayout((vboxlayout))
        # get the video to output on the window
        self.mediaplayer.setVideoOutput(videowidget)


    # To choose file from Pc method & enabling the play button
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename!= '':
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)


    # If the video is paued clicking play button enables it, else if it's playing clicking play button pauses it
    def play_video(self):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()


        else:
            self.mediaplayer.play()
            print("played")

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())




















#Initiate the application
app=QApplication(sys.argv)
#Make an instance of the Window class
window=Window()
sys.exit(app.exec_())




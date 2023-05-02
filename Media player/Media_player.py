import sys
from PyQt6.QtWidgets import ( QApplication,QWidget, QMainWindow, QVBoxLayout, QPushButton, 
                             QSlider, QHBoxLayout, QLabel, QStyle, QSizePolicy, QFileDialog, QListWidget,QComboBox)
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt 
from PyQt6.QtGui import QIcon,QPalette

# Issues to address:
# 1. Not playing audio but only video with mp4
# 2. On click implementation to be added to the scenes list 

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(350, 100, 1000 , 700)

        self.init_ui()

        self.show()

    def init_ui(self):

        #self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player = QMediaPlayer()
        video_widget = QVideoWidget()
        video_widget.resize(700,500)

        open_button = QPushButton("Open")
        open_button.clicked.connect(self.open_file)
        #self.play_button.setEnabled(False)

        self.play_button = QPushButton("Play")
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self.play_video)
        #self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.pause_button = QPushButton("Pause")
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.pause_video)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_video)


        self.pageCombo = QComboBox()
        self.pageCombo.addItems(["Page 1", "Page 2"])

        hbox_layout = QHBoxLayout()
        hbox_layout.setContentsMargins(0,0,0,0)
        hbox_layout.addWidget(open_button)
        hbox_layout.addWidget(self.play_button)
        hbox_layout.addWidget(self.pause_button)
        hbox_layout.addWidget(self.stop_button)
        

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.pageCombo)
        vbox_layout.addWidget(video_widget)
        vbox_layout.addLayout(hbox_layout)
      

        self.setLayout(vbox_layout)
        self.media_player.setVideoOutput(video_widget)

    def open_file(self):
        filename,_ =  QFileDialog.getOpenFileName(self,"Open Video")

        if filename !='':
            self.media_player.setSource(QUrl.fromLocalFile(filename))
            self.play_button.setEnabled(True)
            #self.media_player.play()

    def play_video(self):
        self.media_player.play()
        self.pause_button.setEnabled(True)
        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def pause_video(self):
        self.media_player.pause()
        self.pause_button.setEnabled(False)
        self.play_button.setEnabled(True)

    def stop_video(self):
        self.media_player.stop()
        self.stop_button.setEnabled(False)
        self.play_button.setEnabled(True)


 

    #     #self.media_player.setVideoOutput(self.video_widget)
    #     #self.video_widget = QVideoWidget()
    #     self.media_player.setVideoOutput(self.video_widget)
    #    # self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("Video.mp4")))
    #     self.media_player.positionChanged.connect(self.position_changed)
    #     self.media_player.durationChanged.connect(self.duration_changed)

    #     container = QWidget()
    #     container.setLayout(layout)
    #     self.setCentralWidget(container)

    # def set_position(self, position):
    #     self.media_player.setPosition(position)

    # def position_changed(self, position):
    #     self.slider.setValue(position)

    # def duration_changed(self, duration):
    #     self.slider.setRange(0, duration)
   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    sys.exit(app.exec())

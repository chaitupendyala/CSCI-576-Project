import sys
from PyQt6.QtWidgets import ( QApplication,QWidget, QMainWindow, QVBoxLayout, QPushButton, 
                             QSlider, QHBoxLayout, QLabel, QStyle, QSizePolicy, QFileDialog, QListWidget,QComboBox)
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt 
from PyQt6.QtGui import QIcon,QPalette

# from scenedetection import SceneDetech

# Issues to address:
# 1. Not playing audio but only video with mp4

class Media_player(QWidget):
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

        self.merged_time = []
        
        # self.slider = QSlider(Qt.Orientation.Horizontal)
        # self.slider.setRange(0,0)

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
        self.pageCombo.activated.connect(self.setTime)

        hbox_layout = QHBoxLayout()
        hbox_layout.setContentsMargins(0,0,0,0)
        hbox_layout.addWidget(open_button)
        hbox_layout.addWidget(self.play_button)
        hbox_layout.addWidget(self.pause_button)
        hbox_layout.addWidget(self.stop_button)
        

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.pageCombo)
        vbox_layout.addWidget(video_widget)
        # vbox_layout.addWidget(self.slider)
        vbox_layout.addLayout(hbox_layout)
        
      

        self.setLayout(vbox_layout)
        self.media_player.setVideoOutput(video_widget)

       # self.media_player.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename,_ =  QFileDialog.getOpenFileName(self,"Open Video")

        if filename !='':
            self.media_player.setSource(QUrl.fromLocalFile(filename))
            # scenedetect = SceneDetech(__file__=filename)
            # self.scenes = scenedetect.run_scene_detection()
            self.scenes = {'SCENES': [10000,50000], 
                            'SHOTS': [20000,60000], 
                            'SUBSHOTS': [40000]}
            self.list = []
            self.merged_time = self.scenes['SCENES'] + self.scenes['SHOTS'] + self.scenes['SUBSHOTS']
            self.merged_time.sort()
            print(self.merged_time)
            scene_ind = 0
            shot_ind = 0
            subshot_ind = 0
            for item in self.merged_time:
                if(scene_ind < len(self.scenes['SCENES']) and item == self.scenes['SCENES'][scene_ind]):
                    self.list.append('Scene'+ str(scene_ind+1)) 
                    scene_ind+=1
                elif(shot_ind < len(self.scenes['SHOTS']) and item == self.scenes['SHOTS'][shot_ind]):
                    self.list.append('  Shot'+ str(shot_ind+1)) 
                    shot_ind+=1
                elif(subshot_ind < len(self.scenes['SUBSHOTS']) and item == self.scenes['SUBSHOTS'][subshot_ind]):
                    self.list.append('      Subshot'+ str(subshot_ind+1)) 
                    subshot_ind+=1
            print(self.list)
            self.pageCombo.addItems(self.list)
            self.play_button.setEnabled(True)
            #self.media_player.play()
            self.media_player.duration()

    


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


    # def duration_changed(self, duration):
    #     self.slider.setRange(0, duration)

    def setTime(self):
        pos = self.merged_time[self.pageCombo.currentIndex()]
        self.media_player.setPosition(pos)

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

   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_player = Media_player()
    sys.exit(app.exec())

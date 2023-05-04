import sys
from PyQt5.QtWidgets import ( QApplication,QWidget, QMainWindow, QVBoxLayout, QPushButton, 
                             QSlider, QHBoxLayout, QLabel, QStyle, QSizePolicy, QFileDialog, QListWidget,QComboBox)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt 
from PyQt5.QtGui import QIcon,QPalette

# from scenedetection import SceneDetech


class Media_player(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.setWindowTitle("Video Player")
        self.setGeometry(350, 100, 1000 , 700)
        self.filename = ""

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
    
    def get_file_name(self):
        return self.filename
    
    def video_processed(self, scenes):
        if self.filename !='':
            content = QMediaContent(QUrl.fromLocalFile(self.filename))
            self.media_player.setMedia(content)

            self.scenes = scenes
            self.scenes_ms = {}
            for key in self.scenes:
                self.scenes_ms[key]=[]
                for time in self.scenes[key]:
                    hours, minutes, seconds = time.split(':')
                    seconds, milliseconds = seconds.split('.')

                    hours_in_ms = int(hours) * 60 * 60 * 1000
                    minutes_in_ms = int(minutes) * 60 * 1000
                    seconds_in_ms = int(seconds) * 1000
                    milliseconds = int(milliseconds)
                    total_ms = hours_in_ms + minutes_in_ms + seconds_in_ms + milliseconds
                    self.scenes_ms[key].append(total_ms)
            self.scenes = self.scenes_ms
            self.list = []
            self.merged_time = self.scenes['SCENES'] + self.scenes['SHOTS'] + self.scenes['SUBSHOTS']
            self.merged_time.sort()
            scene_ind = 0
            shot_ind = 0
            subshot_ind = 0
            shot_num = 1
            subshot_num = 1
            for item in self.merged_time:
                if(scene_ind < len(self.scenes['SCENES']) and item == self.scenes['SCENES'][scene_ind]):
                    self.list.append('Scene'+ str(scene_ind+1)) 
                    scene_ind+=1
                    shot_num = 1
                    subshot_num = 1
                elif(shot_ind < len(self.scenes['SHOTS']) and item == self.scenes['SHOTS'][shot_ind]):
                    self.list.append('  Shot'+ str(shot_num)) 
                    shot_ind+=1
                    shot_num+=1
                    subshot_num = 1
                elif(subshot_ind < len(self.scenes['SUBSHOTS']) and item == self.scenes['SUBSHOTS'][subshot_ind]):
                    self.list.append('      Subshot'+ str(subshot_num)) 
                    subshot_ind+=1
                    subshot_num += 1
            self.pageCombo.addItems(self.list)
            self.play_button.setEnabled(True)
            self.media_player.duration()

    def open_file(self):
        self.filename,_ =  QFileDialog.getOpenFileName(self,"Open Video")
        self.controller.file_name_received()

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

    def setTime(self):
        pos = self.merged_time[self.pageCombo.currentIndex()]
        self.media_player.setPosition(pos)   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_player = Media_player()
    sys.exit(app.exec())

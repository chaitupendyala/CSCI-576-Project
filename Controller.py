from create_indexes.scenedetection import SceneDetech
from media_player.media_player import Media_player
import time
import sys
from PyQt5.QtWidgets import QApplication

class Controller:
    def __init__(self) -> None:
        self.file_name = None
        self.media_player = None

    def open_media_player(self):
        self.media_player = Media_player(self)

    def run_scene_detect(self, file_location):
        scene_detect = SceneDetech(file_location=file_location)
        shots = scene_detect.run_scene_detection()
        return shots
    
    def file_name_received(self):
        shots = self.run_scene_detect(file_location=self.media_player.get_file_name())
        self.media_player.video_processed(shots)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.open_media_player()

    sys.exit(app.exec())
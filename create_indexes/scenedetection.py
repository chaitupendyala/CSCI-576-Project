from .AudioSceneDetech import AudioSceneDetech
from .VideoSceneDetech import VideoSceneDetech

class SceneDetech:
    def __init__(self, audio_file_name=None, video_file_name=None) -> None:
        self.audio_file_name = audio_file_name
        self.video_file_name = video_file_name
    
    def run_scene_detection(self):
        pass
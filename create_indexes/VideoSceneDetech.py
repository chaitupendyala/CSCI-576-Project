from scenedetect import detect, ContentDetector
from scenedetect import detect, ThresholdDetector
from scenedetect import detect, AdaptiveDetector

class VideoSceneDetech:
    def __inti__(self, video_file_name=None):
        self.video_file_name = video_file_name

    def detech_scene_change_using_contect_detector(self):
        return detect(self.video_file_name, ContentDetector())

    def detech_scene_change_using_threshold_detector(self):
        return detect(self.video_file_name, ThresholdDetector())

    def detech_scene_change_using_adaptive_detector(self):
        return detect(self.video_file_name, AdaptiveDetector())
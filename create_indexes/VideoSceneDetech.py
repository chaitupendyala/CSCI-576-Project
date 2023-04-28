from scenedetect import detect, ContentDetector
from scenedetect import detect, ThresholdDetector
from scenedetect import detect, AdaptiveDetector

class VideoSceneDetech:
    def __init__(self, video_file_name=None):
        self.video_file_name = video_file_name

    def _detech_scene_change_using_detector(self, detector):
        scenes = detect(self.video_file_name, detector())
        scene_change_points = []
        for scene in scenes:
            scene_change_points.append(scene[1].get_timecode())
        
        return scene_change_points

    def detech_scene_change_using_content_detector(self):
        return self._detech_scene_change_using_detector(ContentDetector)

    def detech_scene_change_using_threshold_detector(self):
        return self._detech_scene_change_using_detector(ThresholdDetector)

    def detech_scene_change_using_adaptive_detector(self):
        return self._detech_scene_change_using_detector(AdaptiveDetector)
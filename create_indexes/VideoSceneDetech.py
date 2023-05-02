from scenedetect import detect, ContentDetector
from scenedetect import detect, ThresholdDetector
from scenedetect import detect, AdaptiveDetector
import cv2
from datetime import datetime, timedelta

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

    @staticmethod
    def add_seconds_to_time_object(time_object, seconds):
        new_time_object = time_object + timedelta(seconds= seconds)
        return new_time_object.strftime('%H:%M:%S.%f')[:-3]
    
    def _entropy_difference(self, time1, time2):
        return None

    def entropy_difference(self, in_times):
        video = cv2.VideoCapture(self.video_file_name)
        for time in in_times:
            time_object = datetime.strptime(time, '%H:%M:%S.%f')
            time1 = f'{self.add_seconds_to_time_object(time_object, -2)}'
            time2 = f'{self.add_seconds_to_time_object(time_object, 2)}'
            entropy_difference = self._entropy_difference(time1, time2)
            print(time, time1, time2)
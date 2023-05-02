from scenedetect import detect, ContentDetector
from scenedetect import detect, ThresholdDetector
from scenedetect import detect, AdaptiveDetector
import cv2
import math
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

    # Extract video frames within the given time window
    def video_frames_in_time_window(self, video_file, start_time, end_time):
        video = cv2.VideoCapture(video_file)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)

        frames = []

        # Print some useful information
        print(f"FPS: {fps}")
        print(f"Total Frames: {total_frames}")
        print(f"Start Frame: {start_frame}")
        print(f"End Frame: {end_frame}")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")

        # Read frames from the video and append them to frames list

        for i in range(end_frame + 1):
            ret, frame = video.read()

            if not ret:
                print(f"Frame {i} not read")
                break

            if i >= start_frame:
                frames.append(frame)

            # Break the loop when the current frame index i is greater than the end_frame
            if i >= end_frame:
                break

        video.release()
        return frames

    # Compare two histograms using the specified method
    def compare_histograms(self, hist1, hist2, method=cv2.HISTCMP_CORREL):
        similarity = cv2.compareHist(hist1, hist2, method)
        return similarity

    # Compute color histogram similarities for consecutive frames in the video
    def compute_color_histogram_similarity(self, video, num_bins=128):
        similarities = []
        for i in range(len(video) - 1):
            frame1 = video[i]
            frame2 = video[i + 1]

            hist1 = cv2.calcHist([frame1], [0, 1, 2], None, [num_bins, num_bins, num_bins], [0, 256, 0, 256, 0, 256])
            hist2 = cv2.calcHist([frame2], [0, 1, 2], None, [num_bins, num_bins, num_bins], [0, 256, 0, 256, 0, 256])

            similarity = self.compare_histograms(hist1, hist2)
            similarities.append(similarity)

        return similarities

    # Calculate the entropy difference between consecutive time windows in the video

    def entropy_difference(self, window_size=2):
        video = cv2.VideoCapture(self.video_file_name)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / fps
        num_windows = int(video_duration / window_size)

        # Loop through all pairs of consecutive time windows
        for i in range(num_windows - 1):
            # Define time windows
            start_time1 = i * window_size
            end_time1 = start_time1 + window_size
            start_time2 = end_time1
            end_time2 = start_time2 + window_size

            # Get video frames for each time window
            video_window1 = self.video_frames_in_time_window(self.video_file_name, start_time1, end_time1)
            video_window2 = self.video_frames_in_time_window(self.video_file_name, start_time2, end_time2)

            # Calculate color histogram similarities for each time window
            similarities_window1 = self.compute_color_histogram_similarity(video_window1)
            similarities_window2 = self.compute_color_histogram_similarity(video_window2)

            # Calculate the average similarity for each time window
            avg_window1 = sum(similarities_window1) / len(similarities_window1) if len(similarities_window1) > 0 else 0
            avg_window2 = sum(similarities_window2) / len(similarities_window2) if len(similarities_window2) > 0 else 0

            # Calculate the entropy for each time window
            entropy_window1 = -avg_window1 * math.log2(avg_window1) if avg_window1 > 0 else 0
            entropy_window2 = -avg_window2 * math.log2(avg_window2) if avg_window2 > 0 else 0

            # Calculate the entropy difference between the two time windows
            entropy_diff = abs(entropy_window1 - entropy_window2)

            print(f"Time Window 1: {start_time1} - {end_time1}")
            print(f"Similarities Window 1: {similarities_window1}")
            print(f"Time Window 2: {start_time2} - {end_time2}")
            print(f"Similarities Window 2: {similarities_window2}")
            print(f"Entropy Difference: {entropy_diff}")
            print("---------------------------------------------------------")

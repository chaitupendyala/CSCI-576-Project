from scenedetect import detect, ContentDetector
from scenedetect import detect, ThresholdDetector
from scenedetect import detect, AdaptiveDetector
import cv2
import math
import numpy as np
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

    @staticmethod
    def convert_to_seconds(timestamp):
        hours, minutes, seconds = map(float, timestamp.split(':'))
        return hours * 3600 + minutes * 60 + seconds

    # Extract video frames within the given time window
    def video_frames_in_time_window(self, video_file, start_time, end_time):
        video = cv2.VideoCapture(video_file)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)

        frames = []

        # Print some useful information
        # print(f"FPS: {fps}")
        # print(f"Total Frames: {total_frames}")
        # print(f"Start Frame: {start_frame}")
        # print(f"End Frame: {end_frame}")
        # print(f"Start Time: {start_time}")
        # print(f"End Time: {end_time}")

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

    def compare_histograms(self, hist1, hist2, method=cv2.HISTCMP_CORREL):
        similarity = cv2.compareHist(hist1, hist2, method)
        return similarity


    def split_frame_into_macroblocks(self, frame, macroblock_size=96):
        height, width, _ = frame.shape
        macroblocks = []

        for y in range(0, height, macroblock_size):
            for x in range(0, width, macroblock_size):
                macroblock = frame[y:y + macroblock_size, x:x + macroblock_size]
                macroblocks.append(macroblock)

        return macroblocks

    def compute_combined_motion_vector_histogram_similarity(self, video, num_bins=16, macroblock_size=96,
                                                            combined_weight=0.8):
        similarities = []

        for i in range(len(video) - 1):
            frame1 = video[i]
            frame2 = video[i + 1]

            macroblocks1 = self.split_frame_into_macroblocks(frame1, macroblock_size)
            macroblocks2 = self.split_frame_into_macroblocks(frame2, macroblock_size)

            macroblock_similarities = []

            for mb1, mb2 in zip(macroblocks1, macroblocks2):
                hist1 = cv2.calcHist([mb1], [0, 1, 2], None, [num_bins, num_bins, num_bins], [0, 256, 0, 256, 0, 256])
                hist2 = cv2.calcHist([mb2], [0, 1, 2], None, [num_bins, num_bins, num_bins], [0, 256, 0, 256, 0, 256])

                flow = cv2.calcOpticalFlowFarneback(cv2.cvtColor(mb1, cv2.COLOR_BGR2GRAY),
                                                    cv2.cvtColor(mb2, cv2.COLOR_BGR2GRAY), None, 0.5, 3, 15, 3, 5, 1.2,
                                                    0)
                magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])

                similarity = self.compare_histograms(hist1, hist2)
                motion_similarity = np.mean(magnitude)

                macroblock_similarities.append((similarity, motion_similarity))

            average_similarity = np.mean([sim[0] for sim in macroblock_similarities])
            average_motion_similarity = np.mean([sim[1] for sim in macroblock_similarities])

            final_similarity = (1 - combined_weight) * average_similarity + combined_weight * average_motion_similarity
            similarities.append(final_similarity)

        return similarities

    def entropy_difference(self, timestamps, window_size=2):

        entropy_differences = []

        for timestamp in timestamps:
            current_time = self.convert_to_seconds(timestamp)
            start_time1 = current_time - window_size
            end_time1 = current_time
            start_time2 = current_time
            end_time2 = current_time + window_size

            video_window1 = self.video_frames_in_time_window(self.video_file_name, start_time1, end_time1)
            video_window2 = self.video_frames_in_time_window(self.video_file_name, start_time2, end_time2)

            similarities_window1 = self.compute_combined_motion_vector_histogram_similarity(video_window1)
            similarities_window2 = self.compute_combined_motion_vector_histogram_similarity(video_window2)

            avg_window1 = sum(similarities_window1) / len(similarities_window1) if len(similarities_window1) > 0 else 0
            avg_window2 = sum(similarities_window2) / len(similarities_window2) if len(similarities_window2) > 0 else 0

            similarity_diff = abs(avg_window1 - avg_window2)

            entropy_differences.append(similarity_diff)

        return entropy_differences

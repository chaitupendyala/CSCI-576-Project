from AudioSceneDetech import AudioSceneDetech
from VideoSceneDetech import VideoSceneDetech
from constants import *
import numpy as np

dataset_locations = {
    READY_PLAYER_ONE: {
        AUDIO_FILE: f"../{DATA_SET_LOCATION}/{READY_PLAYER_ONE}/{AUDIO_FILE}",
        VIDEO_FILE_MP4: f"../{DATA_SET_LOCATION}/{READY_PLAYER_ONE}/{VIDEO_FILE_MP4}",
        VIDEO_FILE_RGB: f"../{DATA_SET_LOCATION}/{READY_PLAYER_ONE}/{VIDEO_FILE_RGB}"
    },
    THE_GREAT_GATSBY: {
        AUDIO_FILE: f"../{DATA_SET_LOCATION}/{THE_GREAT_GATSBY}/{AUDIO_FILE}",
        VIDEO_FILE_MP4: f"../{DATA_SET_LOCATION}/{THE_GREAT_GATSBY}/{VIDEO_FILE_MP4}",
        VIDEO_FILE_RGB: f"../{DATA_SET_LOCATION}/{THE_GREAT_GATSBY}/{VIDEO_FILE_RGB}"
    },
    THE_LONG_DARK: {
        AUDIO_FILE: f"../{DATA_SET_LOCATION}/{THE_LONG_DARK}/{AUDIO_FILE}",
        VIDEO_FILE_MP4: f"../{DATA_SET_LOCATION}/{THE_LONG_DARK}/{VIDEO_FILE_MP4}",
        VIDEO_FILE_RGB: f"../{DATA_SET_LOCATION}/{THE_LONG_DARK}/{VIDEO_FILE_RGB}"
    }
}


class SceneDetech:
    def __init__(self, data_set=None, file_location=None) -> None:
        self.data_set = data_set
        self.file_location = file_location
        self.videoSceneDetech = None
        self.audioSceneDetect = None

    # def compute_scene_shot_subshot_thresholds(self, entropies, scene_percentile=80, shot_percentile=10):
    #     return (np.percentile(entropies, scene_percentile), np.percentile(entropies, shot_percentile))

    def compute_video_entropies(self, video_change_times):
        entropy_differences = self.videoSceneDetech.entropy_difference(timestamps=video_change_times, window_size=2)
        return entropy_differences

    def compute_scene_shot_subshot_thresholds(self, video_entropies, scene_std_multiplier=1, shot_std_multiplier=0.2):
        entropies_mean = np.mean(video_entropies)
        entropies_std = np.std(video_entropies)

        scene_threshold = entropies_mean + scene_std_multiplier * entropies_std
        shot_threshold = entropies_mean - shot_std_multiplier * entropies_std

        return scene_threshold, shot_threshold

    def run_scene_detection(self):
        if self.file_location == None and (self.data_set == None or self.data_set not in dataset_locations):
            print("Please provide a dataset")
            return

        if self.file_location != None:
            self.videoSceneDetech = VideoSceneDetech(video_file_name=self.file_location)
            self.audioSceneDetect = AudioSceneDetech(self.file_location)

        else:
            self.videoSceneDetech = VideoSceneDetech(video_file_name=dataset_locations[self.data_set][VIDEO_FILE_MP4])
            self.audioSceneDetect = AudioSceneDetech(dataset_locations[self.data_set][AUDIO_FILE])

        scene_changes_content_detector = self.videoSceneDetech.detech_scene_change_using_content_detector()
        scene_changes_adaptive_detector = self.videoSceneDetech.detech_scene_change_using_adaptive_detector()

        scene_change_points = set()
        for scene in scene_changes_content_detector:
            scene_change_points.add(scene)

        for scene in scene_changes_adaptive_detector:
            scene_change_points.add(scene)


        scene_change_points = sorted(list(scene_change_points))

        # Filter nearby timestamps
        scene_change_points = self.videoSceneDetech.filter_nearby_timestamps(scene_change_points)

        audio_entropies = self.audioSceneDetect.compute_audio_entropies(scene_change_points)

        video_entropies = self.compute_video_entropies(video_change_times=scene_change_points)

        video_threshold_scene, video_threshold_shot = self.compute_scene_shot_subshot_thresholds(video_entropies,
                                                                                                 scene_std_multiplier=1,
                                                                                                 shot_std_multiplier=0.7)

        audio_threshold_scene, audio_threshold_shot = self.compute_scene_shot_subshot_thresholds(audio_entropies,
                                                                                                 scene_std_multiplier=.5,
                                                                                                 shot_std_multiplier=.1)

        shots = {"SCENES": ['00:00:00.000'], "SHOTS": [], "SUBSHOTS": []}

        for i in range(len(video_entropies)):
            current_audio_entropy = audio_entropies[i]
            current_video_entropy = video_entropies[i]
            # if current_video_entropy >= video_threshold_scene and current_audio_entropy >= audio_threshold_scene:
            #     shots["SCENES"].append(scene_change_points[i])
            # elif (current_video_entropy < video_threshold_scene and current_video_entropy >= video_threshold_shot) and \
            #      (current_audio_entropy < audio_threshold_shot):
            #     shots["SHOTS"].append(scene_change_points[i])
            # else:
            #     shots["SUBSHOTS"].append(scene_change_points[i])
            # if current_video_entropy >= video_threshold_scene and current_audio_entropy >= audio_threshold_scene:
            #     shots["SCENES"].append(scene_change_points[i])
            # elif current_audio_entropy < audio_threshold_scene and current_video_entropy >= video_threshold_scene:
            #     shots["SHOTS"].append(scene_change_points[i])
            # elif current_audio_entropy < audio_threshold_scene and current_video_entropy < video_threshold_scene:
            #     shots["SUBSHOTS"].append(scene_change_points[i])
            # else:
            #     shots["SUBSHOTS"].append(scene_change_points[i])
            if current_video_entropy >= video_threshold_scene:
                shots["SCENES"].append(scene_change_points[i])
            elif current_video_entropy < video_threshold_scene and current_video_entropy >= video_threshold_shot:
                shots["SHOTS"].append(scene_change_points[i])
            else:
                shots["SUBSHOTS"].append(scene_change_points[i])

        return shots


def main():
    sceneDetech = SceneDetech(READY_PLAYER_ONE)

    scene_changes = sceneDetech.run_scene_detection()
    print(scene_changes)

    # videoSceneDetechController = VideoSceneDetech(video_file_name = dataset_locations[READY_PLAYER_ONE][VIDEO_FILE_MP4])
    # entropy_differences = videoSceneDetechController.entropy_difference(timestamps=video_times, window_size=2)


if __name__ == '__main__':
    main()

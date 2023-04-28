from AudioSceneDetech import AudioSceneDetech
from VideoSceneDetech import VideoSceneDetech
from constants import *

dataset_locations = {
    READY_PLAYER_ONE : {
        AUDIO_FILE : f"../{DATA_SET_LOCATION}/{READY_PLAYER_ONE}/{AUDIO_FILE}",
        VIDEO_FILE_MP4: f"../{DATA_SET_LOCATION}/{READY_PLAYER_ONE}/{VIDEO_FILE_MP4}",
        VIDEO_FILE_RGB: f"../{DATA_SET_LOCATION}/{READY_PLAYER_ONE}/{VIDEO_FILE_RGB}"
    },
    THE_GREAT_GATSBY : {
        AUDIO_FILE : f"../{DATA_SET_LOCATION}/{THE_GREAT_GATSBY}/{AUDIO_FILE}",
        VIDEO_FILE_MP4: f"../{DATA_SET_LOCATION}/{THE_GREAT_GATSBY}/{VIDEO_FILE_MP4}",
        VIDEO_FILE_RGB: f"../{DATA_SET_LOCATION}/{THE_GREAT_GATSBY}/{VIDEO_FILE_RGB}"
    },
    THE_LONG_DARK : {
        AUDIO_FILE : f"../{DATA_SET_LOCATION}/{THE_LONG_DARK}/{AUDIO_FILE}",
        VIDEO_FILE_MP4: f"../{DATA_SET_LOCATION}/{THE_LONG_DARK}/{VIDEO_FILE_MP4}",
        VIDEO_FILE_RGB: f"../{DATA_SET_LOCATION}/{THE_LONG_DARK}/{VIDEO_FILE_RGB}"
    }
}

class SceneDetech:
    def __init__(self, data_set=None) -> None:
        self.data_set = data_set
    
    def run_scene_detection(self):
        if self.data_set == None or self.data_set not in dataset_locations:
            print("Please provide a dataset")
            return

        videoSceneDetech = VideoSceneDetech(video_file_name = dataset_locations[self.data_set][VIDEO_FILE_MP4])
        audioSceneDetect = AudioSceneDetech(dataset_locations[self.data_set][AUDIO_FILE])

        scene_changes_content_detector = videoSceneDetech.detech_scene_change_using_content_detector()
        scene_changes_adaptive_detector = videoSceneDetech.detech_scene_change_using_adaptive_detector()

        scene_change_points = set()
        for scene in scene_changes_content_detector:
            scene_change_points.add(scene)
        
        for scene in scene_changes_adaptive_detector:
            scene_change_points.add(scene)
        
        return list(scene_change_points)

def main():
    sceneDetech = SceneDetech(READY_PLAYER_ONE)

    print(sceneDetech.run_scene_detection())

if __name__ == '__main__':
    main()

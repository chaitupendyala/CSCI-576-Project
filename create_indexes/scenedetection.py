import subprocess
#import scenedetect
#pip install scenedetect[opencv] --upgrade
import cv2



print("Generic Scene Detection:")
# generic scene splitting 
from scenedetect import detect, ContentDetector
scene_list = detect('InputVideo.mp4', ContentDetector())

for i, scene in enumerate(scene_list):
    print('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
        i+1,
        scene[0].get_timecode(), scene[0].get_frames(),
        scene[1].get_timecode(), scene[1].get_frames(),))
  
  
################################################################
print("Splitting scenes while taking into account fading frames:")
from scenedetect import detect, ThresholdDetector
scene_list = detect('InputVideo.mp4', ThresholdDetector())
  
for i, scene in enumerate(scene_list):
    print('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
        i+1,
        scene[0].get_timecode(), scene[0].get_frames(),
        scene[1].get_timecode(), scene[1].get_frames(),))
    
    
################################################################    
print("Splitting scenes while taking into account fast camera movements:")
from scenedetect import detect, AdaptiveDetector
scene_list = detect('InputVideo.mp4', AdaptiveDetector())
  
for i, scene in enumerate(scene_list):
    print('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
        i+1,
        scene[0].get_timecode(), scene[0].get_frames(),
        scene[1].get_timecode(), scene[1].get_frames(),))

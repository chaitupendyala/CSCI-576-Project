import subprocess
#import scenedetect
#pip install scenedetect[opencv] --upgrade
import cv2


###############################################################################         
# manipulating the scenes, shots, and subshots using the SceneDetect Library #
###############################################################################    

from scenedetect import detect, AdaptiveDetector

# examining 'ImputVideo.mp4'
# adaptive_threshold=1.5
# min_scene_len=2
scene_list = detect('InputVideo.mp4', AdaptiveDetector())

# parse through all the scenes detected from the AdaptiveDetector() function:
for i, scene in enumerate(scene_list):
    
    ## calculating the length of time for each interval
    ## calculating the calculate the number of frames for each internval 
    temp = scene[1].get_frames()-scene[0].get_frames()
    time1 = scene[1].get_timecode()
    time1a = time1[3:5]
    time1int = int (time1a)*60
    time1 =time1[6:len(time1)]
    time1full= time1int+float (time1)
    
    time2 = scene[0].get_timecode()
    time2a = time2[3:5]
    time2int = int (time2a)*60
    time2 =time2[6:len(time2)]
    time2full= time2int+ float (time2)
    time = float (time1full)-float (time2full)
    
                      
    if temp>=0:
        ## if time intervals aren't too short or long
        if time>1 and time<10:
            ## divide the scene and shot differences depending on benchmark value
            if temp>=700:
                print('Scene Change: Breakpoint %2d: Time %s / Frame %d' % (
                    i+1,
                    scene[1].get_timecode(), scene[1].get_frames(),))
   
            else:
                print('    Shot Change: Breakpoint %2d: Time %s / Frame %d' % (
                    i+1,
                    scene[1].get_timecode(), scene[1].get_frames(),))
         
        else:
            
            ## we could probaby take this out, I was just trying to make sure that 
            ## everything was getting picked up
            if temp>=700:
                print('Scene Change: Breakpoint %2d: Time %s / Frame %d' % (
                    i+1,
                    scene[1].get_timecode(), scene[1].get_frames(),))
             
            ## intervals exeedingly short or long will be picked up as subshots 
            else:
                print('            Subshot: Breakpoint %2d: Time %s / Frame %d' % (
                        i+1,
                        scene[1].get_timecode(), scene[1].get_frames(),))
             
print()




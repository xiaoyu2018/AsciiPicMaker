import cv2
from PIL import Image
import os
import shutil


MATERIAL_DIR = './materials/'
          

class VideoSpliter:
    def __init__(self, path:str):
        self.path = path
        self.video = cv2.VideoCapture(path)

    def split(self , interval):
        save_dir=MATERIAL_DIR+'images/video_split/'+self.path.split('/')[-1].split('.')[0]+"/"

        if(os.path.exists(save_dir)):
            shutil.rmtree(save_dir)
        os.makedirs(save_dir)
        
        i=0
        j=0
        while(True):
            sucess , frame = self.video.read()
            
            if(not sucess):
                print("video is all read")
                break
            
            if(i==interval):
                cv2.imwrite(save_dir+str(j)+'.jpg',frame)
                i=0
                j+=1

            i+=1

if __name__=='__main__':
    # vs=VideoSpliter("./materials/videos/test.mp4")
    # vs.split(5)
    pass
import cv2
import os
import shutil


MATERIAL_DIR = './materials/'
OUTPUT_DIR = './outputs/'          

class VideoSProcessor:
    def __init__(self):
        pass
    
    def split(self , video_path:str ,interval=1):
        video=cv2.VideoCapture(video_path)
        save_dir=MATERIAL_DIR+'images/video_split/'+video_path.split('/')[-1].split('.')[0]+"/"

        if(os.path.exists(save_dir)):
            shutil.rmtree(save_dir)
        os.makedirs(save_dir)
        
        i=0
        j=0
        while(True):
            sucess , frame = video.read()
            
            if(not sucess):
                print("video is all read")
                break
            
            if(i==interval):
                cv2.imwrite(save_dir+str(j)+'.jpg',frame)
                i=0
                j+=1

            i+=1

    def compose(self, img_dir,video_name,fps=30):
        
        files = [img_dir+img for img in os.listdir(img_dir) if img.endswith(".jpg")]
        
        size=cv2.imread(files[0]).shape
        out_path=OUTPUT_DIR+video_name+".mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # mp4
        videoWriter = cv2.VideoWriter(out_path,fourcc=fourcc,fps=fps,frameSize=(size[1],size[0]))

        for file in files:
            img=cv2.imread(file)
            videoWriter.write(img)
            
        videoWriter.release()
        print("composed video is saved in "+out_path)

if __name__=='__main__':
    
    vs=VideoSProcessor()
    vs.split("./materials/videos/dha.mp4",interval=3)
    vs.compose(MATERIAL_DIR+'images/video_split/dha/',"dha_coomposed")
    
    pass
import os
from processor import VideoSProcessor
from converter import Converter
from PIL import Image
import shutil

SPLTI_INTERVAL=1
SAMPLE_RATE = 0.35
RENDERING_FPS=18

vp=VideoSProcessor()
ctr=Converter()


def split_video(video_path, interval=SPLTI_INTERVAL):
    vp.split(video_path, interval)

def compose_video(img_dir, video_name):
    vp.compose(img_dir, video_name)

def convert_one_image(img_path, ascii_path ,is_colorful=True):
    ctr.convert(img_path, is_colorful)
    
    ctr.save(ascii_path)

    ctr.show_pyplot()
    

def online_show(imgs_dir, is_colorful=True):
    files=[img for img in os.listdir(imgs_dir) if img.endswith(".jpg")]
    imgs=[Image.open(imgs_dir+file) for file in files]
    
    for img in imgs:
        ctr.convert(img,is_colorful=is_colorful,sample_rate=0.1)
        ctr.show_pyplot(interval=0.03)
    
def convert_images(imgs_dir, is_colorful=True, sample_rate=SAMPLE_RATE):
    files=[img for img in os.listdir(imgs_dir) if img.endswith(".jpg")]
    imgs=[Image.open(imgs_dir+file) for file in files]
    save_dir="./outputs/images/"+imgs_dir.split("/")[-1]+"/"
    if(os.path.exists(save_dir)):
        shutil.rmtree(save_dir)
    os.makedirs(save_dir)
    
    i=0
    for img in imgs:
        ctr.convert(img,is_colorful=is_colorful,sample_rate=sample_rate)
        ctr.save(save_dir+str(i)+".jpg")
        i+=1
    print("all imgs r converted")
    return save_dir


def offline_show(images_dir):
    vp.compose(images_dir, "output",fps=RENDERING_FPS)

if __name__=='__main__':
    split_video("./materials/videos/dha.mp4")
    convert_images("./materials/images/video_split/dha/")
    offline_show("./outputs/images/")
    pass
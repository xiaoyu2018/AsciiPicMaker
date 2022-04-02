import os
from processor import VideoSProcessor
from converter import Converter
from PIL import Image
import shutil

# 视频抽帧间隔（秒）
SPLTI_INTERVAL=2
# 对原图的下采样比例
SAMPLE_RATE = 0.35
# 合成视频的帧率
RENDERING_FPS=18

vp=VideoSProcessor()
ctr=Converter()


def split_video(video_path, interval=SPLTI_INTERVAL):
    """
    对指定视频抽帧并保存
    """
    vp.split(video_path, interval)

def compose_video(img_dir, video_name):
    """
    将视频帧合成为视频
    """
    vp.compose(img_dir, video_name)

def convert_one_image(img_path, ascii_path ,is_colorful=True):
    """
    将指定单张图片转化为字符画
    """
    img=Image.open(img_path)
    ctr.convert(img, is_colorful,sample_rate=SAMPLE_RATE)
    
    ctr.save(ascii_path)

    ctr.show_pyplot()
    input("ascii pic has been generated.\npress any key to exit...")
    

def online_show(imgs_dir, is_colorful=True ,is_console=False):
    """
    将指定文件下的视频帧实时渲染为字符画视频
    """
    files=[img for img in os.listdir(imgs_dir) if img.endswith(".jpg")]
    imgs=[Image.open(imgs_dir+file) for file in files]
    
    if(is_console):
        for img in imgs:
            ctr.convert(img,is_colorful=is_colorful,sample_rate=0.1)
            ctr.show_console()
    else:
        for img in imgs:
            ctr.convert(img,is_colorful=is_colorful,sample_rate=0.1)
            ctr.show_pyplot(interval=0.03)
    
def convert_images(imgs_dir, is_colorful=True, sample_rate=SAMPLE_RATE):
    """
    将指定文件夹下的所有图片转换为字符画
    """
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



if __name__=='__main__':
    # split_video("./materials/videos/dha.mp4")
    # convert_images("./materials/images/video_split/dha/")
    # compose_video("./outputs/images/")
    # online_show("./materials/images/video_split/dha/")
    convert_one_image("./materials/images/1.jpg","1_ascii.jpg",is_colorful=False)
    pass

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from matplotlib import pyplot as plt

SAMPLE_RATE = 0.6

class Converter:
    def __init__(self, font_style=None,font_size=12):
        # 设置字体风格和大小
        if font_style is None:
            self.font = ImageFont.load_default()
        else:
            self.font = ImageFont.truetype(font_style, font_size)
        # 设置可用转换字符列表，按期望亮度大小升序排列
        self.symbols = np.array(list(" .,-=vM#@"))
        
        self.raw_img=None
        self.ascii_img=None
        self.ascii_mat=None
        
        self.fig=None

    def init_pyplot(self):
        plt.ion()
        fig=plt.figure("output")
        self.fig = fig

        
    def convert(self,raw_img,is_colorful=True,sample_rate=SAMPLE_RATE):
        self.raw_image=raw_img
        img=self.raw_image
        
        # 计算当前字体下字母的纵横比
        aspect_ratio = self.font.getsize("x")[0] / self.font.getsize("x")[1]
        
        # 使图片适应字体纵横比
        new_img_size = np.array(
            [img.size[0] * sample_rate, img.size[1] * sample_rate * aspect_ratio]
        ).astype(int)
        img = self.raw_image.resize(new_img_size)
        
        # 为彩色字符画图片保留副本
        self.raw_img = np.array(img)

        # 将原图转换为灰度图
        img = img.convert("L")
        img=np.array(img)
        
        # 规范化像素灰度取值范围，将其限制在字符列表大小以内的整数值
        img = ((img - img.min()) / (img.max() - \
            img.min()) * (self.symbols.size - 1)).astype(int)
        
        # 保持位置不变，将每个像素映射为字符
        self.ascii_mat=self.symbols[img.astype(int)]
        
        letter_size = self.font.getsize("x")
        img_out_size = new_img_size * letter_size
        bg_color = "black"

        ascii_img=Image.new("RGB", tuple(img_out_size), bg_color)
        draw = ImageDraw.Draw(ascii_img)
        
        # 在新图片上画出所有字符
        y = 0
        for i, line in enumerate(self.ascii_mat):
            for j, ch in enumerate(line):
                if(is_colorful):
                    color = tuple(self.raw_img[i, j])  # 从图片副本中采样颜色
                    draw.text((letter_size[0] * j, y), ch[0], fill=color, font=self.font)
                else:
                    draw.text((letter_size[0] * j, y), ch[0], font=self.font)
            y += letter_size[1]  
    
        self.ascii_img=ascii_img

    def show_console(self):
        """
        字符画显示于控制台
        """
        os.system("cls")
        if(self.ascii_mat is None):
            print("不存在转换结果,请先调用convert方法...")
            return
        for line in self.ascii_mat:
            for i in line:
                print(i,end="")
            print()

    def show_pyplot(self,interval=0.1):
        """
        字符画显示于pyplot
        """
        if(not self.ascii_img):
            print("不存在转换结果,请先调用convert方法...")
            return
        
        if(not self.fig):
            self.init_pyplot()
        
        self.fig.clf()
        ax = self.fig.add_subplot(1, 1, 1)
        ax.axis('off')
        
        ax.imshow(self.ascii_img, cmap='gray')
        ax.plot()

        plt.pause(interval)

    def save(self,save_path):
        self.ascii_img.save(save_path)




if __name__=="__main__":
    
    converter=Converter()
    
    converter.convert("./materials/images/1.jpg",is_colorful=True,sample_rate=0.8)
    converter.show_pyplot()

    input()
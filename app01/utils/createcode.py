#!/usr/bin/env python
#-*- coding:utf-8 -*-

#_*_coding:utf-8_*_


from PIL import Image,ImageDraw,ImageFont,ImageFilter  #pillow

import random
import math, string


#字体的位置，不同版本的系统会有不同
font_path = r'D:\python\rbac\app01\static\fonts\msyhbd.ttf'
#font_path = '/Library/Fonts/Hanzipen.ttc'
#生成几位数的验证码
number = 5
#生成验证码图片的高度和宽度
size = (100,34)
#背景颜色，默认为白色
bgcolor = (255,255,255)
#字体颜色，默认为蓝色
# fontcolor = (0,0,255)
fontcolor = "#000000"
#干扰线颜色。默认为红色
# linecolor = (255,0,0)
linecolor = "#6389C8"
#是否要加入干扰线
draw_line = True
#加入干扰线条数的上下限
line_number = (10,15)




def gen_text():
    source = list(string.ascii_letters)
    for index in range(0,10):
        source.append(str(index))   #把0-9填充到列表中
    return ''.join(random.sample(source,number))#number是生成验证码的位数 从列表随机选择5位数


#用来绘制干扰线
def gene_line(draw,width,height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill = linecolor,width=1)  #在变量xy列表所表示的坐标之间画线。两个坐标中划线[(x,y),(x,y)] width=1 干扰线粗线

def gene_code():
    width,height = size #宽和高
    image = Image.new('RGBA',(width,height),bgcolor) #创建图片

    font = ImageFont.truetype(font_path,25) #验证码的字体和字体大小
    #font = ImageFont.truetype(25) #验证码的字体和字体大小
    draw = ImageDraw.Draw(image) #创建画笔
    #text = "我是中国人" #生成字符串
    text = gen_text() #生成字符串
    font_width, font_height = font.getsize(text)
    # 通过draw.text方法，设置图片上字符串的x,y坐标，字符串，颜色，字体（for循环5次，生成5个字符的验证码)
    draw.text(((width - font_width) / number, (height - font_height) / number),text,font= font,fill=fontcolor) #参数解释，位置，文本内容，颜色 ，font字体 填充字符串
    if draw_line:
        line_number=random.randint(8,12)
        for line in range(line_number):
            gene_line(draw, width, height)

    #http://www.x-faded.com/2018/04/12/python%E5%9B%BE%E5%83%8F%E6%93%8D%E4%BD%9C%E7%9A%84%E5%BA%93pil%EF%BC%8C%E5%B8%B8%E7%94%A8%E4%B8%89%E4%B8%AA%E6%A8%A1%E5%9D%97image%EF%BC%8Cimagedraw%EF%BC%8Cimagefont/
    image = image.transform((width + 20, height +10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强

    # #写入文件
    # path='%s\\\\%s.png' %(save_path,filename)
    # print(path)
    # image.save(path)  # 保存验证码图片
    # print("savepath:",save_path)


    #写入内存
    from io import BytesIO
    f = BytesIO()
    image.save(f, 'png')
    # 取出文件
    data = f.getvalue()
    import base64
    return base64.b64encode(data),text

if __name__ == "__main__":
    imgdata, code=gene_code('D:\\\\python\\\\rbac\\\\app01\\\\tmp','test')
    print(imgdata, code)


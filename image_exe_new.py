import os
import fitz
import configparser
from PIL import Image
import sys


def clear_image_folder(folder_path):
    if os.path.exists(folder_path):
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)


def pdf_to_image(pdf_path, resolution):

####清空文件夹
    clear_image_folder(output_folder)

####打开pdf文件
    doc = fitz.open(pdf_path)


    for page_number, page in enumerate(doc, start=1):
        # 生成像素地图，并考虑到转换分辨率
        pix = page.get_pixmap(matrix=fitz.Matrix(resolution / X_scale, resolution /Y_scale))

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 为每一页生成输出文件路径
        output_path = os.path.join(output_folder, f"page_{page_number}.png")

        # img是Pillow图像，我们可以直接保存，不必转换成OpenCV图像
        img.save(output_path)

    # 在处理完后可选择关闭文档

    doc.close()



if __name__ == "__main__":
    # 创建配置解析器对象
    config = configparser.ConfigParser()
    # 读取config.ini配置文件
    config.read('D:\image_process\config1.ini')

    # 获取settings部分的image_path配置项
    output_folder = config.get('image','path')

    # 检查"image"目录是否存在，如果不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 从命令行获取PDF文件路径
    pdf_path = sys.argv[1]


    # 获取image部分的配置项
    resolution = config.getint('image', 'dpi')
    X_scale = config.getint('image', 'x')
    Y_scale = config.getint('image', 'y')

    # 调用pdf_to_image函数处理pdf文件
    pdf_to_image(pdf_path, resolution)
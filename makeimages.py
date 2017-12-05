#! python3
# coding: UTF-8

import os
from PIL import Image


def create_image(path, width, height):
    pri_img = os.path.join(path, 'origin.png')
    resize_img = Image.open(pri_img).resize((width, height), Image.ANTIALIAS)

    resize_img.save(path+"/png_{width}x{height}.png".format(width=width, height=height))
    resize_img.save(path+"/gif_{width}x{height}.gif".format(width=width, height=height))
    resize_img.save(path+"/webp_{width}x{height}.webp".format(width=width, height=height), "WEBP")
    if len(resize_img.split()) == 4:
        r, g, b, a = resize_img.split()  # 利用split和merge将通道从四个转换为三个
        jpg_img = Image.merge("RGB", (r, g, b))
        jpg_img.save(path+"/jpg_{width}x{height}.jpg".format(width=width, height=height))
    #动图
    motion_img = []
    motion_img.append(resize_img)
    motion_img.append(resize_img.rotate(45))
    motion_img.append(resize_img.rotate(90))
    motion_img.append(resize_img.rotate(135))
    motion_img.append(resize_img.rotate(180))
    motion_img.append(resize_img.rotate(225))
    motion_img.append(resize_img.rotate(270))
    motion_img.append(resize_img.rotate(315))
    resize_img.save(path+"/m_gif_{width}x{height}.gif".format(width=width, height=height),
                    save_all=True,
                    append_images=motion_img,
                    loop=0,
                    transparency=0,
                    disposal=2)
    print("images in " + path)


if __name__ == "__main__":
    in_width, in_height = (int(x) for x in input("size(w h):").split())
    create_image(r"D:\tester\camera360\test_resource\测试用图\makeimages", in_width, in_height)
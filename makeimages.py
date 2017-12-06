#! python3
# coding: UTF-8

import os
from PIL import Image

DEFAULT_ORIGIN_IMAGE = r"F:\github\Py_workspace\img\origin.png"
SUPPORT_SUFFIX = ("png", "gif", "webp", "jpg")

class ImageMaker(object):

    def __init__(self, origin_img):
        self.origin_img = origin_img
        if self._check_origin_image():
            print("load origin image success")
            self.path = os.path.split(self.origin_img)[0]
            self.name = os.path.basename(self.origin_img).split(".")[0]
        else:
            print(self.origin_img + " is not a valid image! exit!")
            exit()

    def _check_origin_image(self):
        if os.path.isfile(self.origin_img):
            suffix = os.path.splitext(self.origin_img)[-1]
            if suffix == ".png" or suffix == ".jpg":
                return True
            else:
                print(self.origin_img + " is not png or jpg file")
                return False
        else:
            print(self.origin_img + " is not a file")
            return False


    def create_image(self, width, height):

        resize_img = Image.open(self.origin_img).resize((width, height), Image.ANTIALIAS)
        for suffix in SUPPORT_SUFFIX:
            if suffix == "webp":
                resize_img.save(self.path+"/{name}_{suffix}_{width}x{height}.{suffix}".format(name=self.name,
                                                                                              width=width,
                                                                                              height=height,
                                                                                              suffix=suffix), "webp")
            # png转jpg,处理a通道
            elif suffix == "jpg" and len(resize_img.split()) == 4:
                r, g, b, a = resize_img.split()  # 利用split和merge将通道从四个转换为三个
                jpg_img = Image.merge("RGB", (r, g, b))
                jpg_img.save(
                    self.path + "/{name}_{suffix}_{width}x{height}.{suffix}".format(name=self.name,
                                                                                    width=width,
                                                                                    height=height,
                                                                                    suffix=suffix))
            else:
                resize_img.save(
                    self.path + "/{name}_{suffix}_{width}x{height}.{suffix}".format(name=self.name,
                                                                                    width=width,
                                                                                    height=height,
                                                                                    suffix=suffix))
            print(self.path+"/{name}_{suffix}_{width}x{height}.{suffix}".format(name=self.name, width=width, height=height, suffix=suffix))

        #动图
        motion_img = []
        for i in range(8):
            motion_img.append(resize_img.rotate(45*i))
        resize_img.save(self.path+"/{name}_motion_{width}x{height}.gif".format(name=self.name, width=width, height=height),
                        save_all=True,
                        append_images=motion_img,
                        loop=0,
                        transparency=0,
                        disposal=2)
        print(self.path+"/{name}_motion_{width}x{height}.gif".format(name=self.name, width=width, height=height))


if __name__ == "__main__":

    while True:
        ori_img = input("Input origin image path:")
        if ori_img == "":
            ori_img = DEFAULT_ORIGIN_IMAGE
        print("Set the origin image to " + ori_img)

        image_maker = ImageMaker(ori_img)
        in_width, in_height = (int(x) for x in input("size(w h):").split())
        image_maker.create_image(in_width, in_height)


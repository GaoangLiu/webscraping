# -*- coding: utf-8 -*-

from PIL import Image
import os
import pytesseract
import enchant
import string

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# pre config image, remove background


class OCR:
    def __init__(self):
        pass

    def pre_concert(self, img):
        width, height = img.size
        threshold = 30
        for i in range(0, width):
            for j in range(0, height):
                p = img.getpixel((i, j))
                r, g, b = p
                if r > threshold or g > threshold or b > threshold:
                    img.putpixel((i, j), WHITE)
                else:
                    img.putpixel((i, j), BLACK)
        img.save("pre_fig.jpg")
        return

    def remove_noise(self, img, window=1):
        """remove noise of pre configured image"""
        if window == 1:
            window_x = [1, 0, 0, -1, 0]
            window_y = [0, 1, 0, 0, -1]
        elif window == 2:
            window_x = [-1, 0, 1, -1, 0, 1, 1, -1, 0]
            window_y = [-1, -1, -1, 1, 1, 1, 0, 0, 0]
        width, height = img.size
        for i in range(width):
            for j in range(height):
                box = []

                for k in range(len(window_x)):
                    d_x = i + window_x[k]
                    d_y = j + window_y[k]
                    try:
                        d_point = img.getpixel((d_x, d_y))
                        if d_point == BLACK:
                            box.append(1)
                        else:
                            box.append(0)
                    except IndexError:
                        img.putpixel((i, j), WHITE)
                        continue

                box.sort()
                if len(box) == len(window_x):
                    mid = box[int(len(box) / 2)]
                    if mid == 1:
                        img.putpixel((i, j), BLACK)
                    else:
                        img.putpixel((i, j), WHITE)
        img.save("mov_noise_fig.jpg")
        return

    def image_to_string(self, opened_img):
        '''return: string (recognized captcha)'''
        try:
            result = pytesseract.image_to_string(
                opened_img).strip().strip(string.punctuation).lower()
            # All captchas I've seen on Douban.com are typical English words, hence we use
            # PyEnchant to check whether the recognized word is a real word.  
            d = enchant.Dict("en_US")
            if result and d.check(result):
                return result
            else:
                print(">> Automatically OCR failed, try recognize image manually.")
                Image.open('images/captcha.jpg').show()                
                return input(">> Type in here what you see in the image: ")

                # print('>> Recognized captcha is: ', result)
                # print(">> Not sure about the captcha, return one from the following :",
                #     d.suggest(result))
                # return d.suggest(result)[0]
        except BaseException as ex:
            print(ex)
            return None

    def process_image(self, img_path):
        '''
        return: String (recognized captcha)
        '''
        img = Image.open(img_path)
        self.pre_concert(img)
        self.remove_noise(img, 2)
        return self.image_to_string(img)



if __name__ == '__main__':
    OCR().process('images/captcha.jpg')

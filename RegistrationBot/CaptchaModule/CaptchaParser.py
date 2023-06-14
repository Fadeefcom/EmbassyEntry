import string

from PIL import Image
from operator import itemgetter
import hashlib
import time


class CaptchaParser:
    __image = None
    __convert_image = None
    __histogram = None
    __image1 = None
    __image2 = None

    def __init__(self, path: str):

        self.__image = Image.open(path)
        self.__convert_image = self.__image.convert("P")
        self.__histogram = self.__convert_image.histogram()
        self.__image1 = Image.new("P", self.__convert_image.size, 255)
        self.__image2 = Image.new("P", self.__convert_image.size, 255)

    def parse_letters(self):
        temp = {}
        # values = {}

        # len = 256
        # print(__histogram)
        # for i in range(len(__histogram)):
        #     values[i] = __histogram[i]
        #
        # for j, k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
        #     print(j, k)

        for x in range(self.__convert_image.size[1]):
            for y in range(self.__convert_image.size[0]):
                pix = self.__convert_image.getpixel((y, x))
                temp[pix] = pix
                if pix == 139 and self.__pix_isolated(self.__convert_image, y, x, 139, 3):  # these are the numbers to get
                    self.__image1.putpixel((y, x), 0)
                if pix == 182 and self.__pix_isolated(self.__convert_image, y, x, 182, 1):
                    self.__image2.putpixel((y, x), 0)

        result_image = self.__image_overlay(self.__image1, self.__image2)
        letters = self.__letters_in_image(result_image)
        count = 0
        for letter in letters:
            count += 1
            letter.save('Gif files/%s.gif' % count)
        return letters


    @staticmethod
    def __pix_isolated(convert_image, y, x, pix, pivot) -> bool:
        count = 0
        for x1 in range(-pivot, pivot):
            for y1 in range(-pivot, pivot):
                if (x + x1 > 0 and y + y1 > 0) and (x + x1 < convert_image.size[1] and y + y1 < convert_image.size[0]):
                    pix_t = convert_image.getpixel((y + y1, x + x1))

                    if pix_t == pix:
                        count += 1

        if count > pivot:
            return True
        else:
            return False

    @staticmethod
    def __pix_exists(convert_image, y, x, x1, y1) -> bool:
        if (x + x1 > 0 and y + y1 > 0) and (x + x1 < convert_image.size[1] and y + y1 < convert_image.size[0]):
            pix_t = convert_image.getpixel((y + y1, x + x1))
            if pix_t != 255:
                return True
            else:
                return False

    @staticmethod
    def __image_overlay(image1, image2) -> Image:
        temp_image = Image.new("P", image1.size, 255)

        for x in range(image1.size[1]):
            for y in range(image1.size[0]):
                pix = image1.getpixel((y, x))

                if pix != 255:
                    temp_image.putpixel((y, x), 0)

                    for x1 in range(-1, 1):
                        for y1 in range(-1, 1):
                            if CaptchaParser.__pix_exists(image2, y, x, x1, y1):
                                temp_image.putpixel((y + y1, x + x1), 0)

        return temp_image

    @staticmethod
    def __image_addition(image, image2) -> Image:
        for y in range(image2.size[0]):  # slice across
            for x in range(image2.size[1]):  # slice down
                pix = image2.getpixel((y, x))

                if pix != 255:
                    image.putpixel((y, x), 0)

    @staticmethod
    def __image_subtraction(image, image2) -> Image:
        for y in range(image2.size[0]):  # slice across
            for x in range(image2.size[1]):  # slice down
                pix = image2.getpixel((y, x))

                if pix != 255:
                    image.putpixel((y, x), 255)

    @staticmethod
    def __letters_in_image(image) -> []:
        in_letter = False
        found_letter = False
        start = 0
        end = 0

        letters = []

        for y in range(image.size[0]):  # slice across
            for x in range(image.size[1]):  # slice down
                pix = image.getpixel((y, x))

                if pix != 255:
                    number = CaptchaParser.__surrounding_area(image, x, y, [0] * 200 * 50)
                    # print(number.histogram())
                    # val = number.histogram()
                    if number.histogram()[0] > 20:
                        letters.append(CaptchaParser.__cut_image(number))

                    CaptchaParser.__image_subtraction(image, number)
                    # temp: Image = CaptchaParser.__cut_image(number)
                    # temp.save("Gif files/temp.gif")
                    # image.save("RegistrationBot/Gif files/number1.gif")
                    # input()

        return letters

    @staticmethod
    def __letters_save(letters):
        count = 0
        for letter in letters:
            m = hashlib.md5()
            m.update(("%s%s" % (time.time(), count)).encode())
            path = "RegistrationBot/Gif files/" + "%s.gif" % m.hexdigest()
            letter.save(path)
            count += 1
        return count

    @staticmethod
    def __surrounding_area(image, x, y, visited) -> Image:
        temp_image = Image.new("P", image.size, 255)
        visited[x * y] = 1
        concat_image = []
        # print("into area xy->", x, y)

        # move down
        for x1 in {-1, -2, 0, 1, 2}:
            # move to right
            for y1 in {-1, -2, 0, 1, 2}:
                if x1 == 0 and y1 == 0:
                    temp_image.putpixel((y, x), (255, 0, 0))
                elif CaptchaParser.__pix_exists(image, y, x, x1, y1):
                    temp_image.putpixel((y + y1, x + x1), (255, 0, 0))
                    if visited[(x + x1) * (y + y1)] == 0:
                        concat_image.append(CaptchaParser.__surrounding_area(image, x + x1, y + y1, visited))

        # temp_image.save("RegistrationBot/Gif files/temp.gif")
        # print("temp image save", x, y)
        # input()
        for image in concat_image:
            # image.save("RegistrationBot/Gif files/concat.gif")
            CaptchaParser.__image_addition(temp_image, image)
            # print("concat image save")
            # input()

        return temp_image

    @staticmethod
    def __cut_image(image) -> Image:
        inletter = False
        foundletter = False
        start = 0
        end = 0

        for y in range(image.size[0]):  # slice across
            for x in range(image.size[1]):  # slice down
                pix = image.getpixel((y, x))
                if pix != 255:
                    inletter = True
            if foundletter == False and inletter == True:
                foundletter = True
                start = y

            if foundletter == True and inletter == False:
                foundletter = False
                end = y
                return image.crop((start, 0, end, 50))

            inletter = False

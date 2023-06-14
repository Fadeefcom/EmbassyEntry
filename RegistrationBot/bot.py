import hashlib

import CaptchaModule.CaptchaParser as CaptchaParser
import CaptchaModule.MLvector as MLVector
import CaptchaModule.VectorCompare as VectorCompare
import UserSession.Session as Session
from PIL import Image


class Bot:

    __session = None
    __ml_vector = None
    __captcha_parser = None

    def __init__(self, user_session: Session):
        self.__session = user_session
        self.__ml_vector = MLVector.MLVector()
        self.__ml_vector.model_training(user_session.GetImageMLPath())
        self.__captcha_parser = CaptchaParser.CaptchaParser(self.__session.GetImagePath())

    def possible_letters(self):
        letters = self.__captcha_parser.parse_letters()
        imageset = self.__ml_vector.get_imageset()
        im = Image.open(self.__session.GetImagePath())
        im2 = Image.new("P", im.size, 255)

        count = 0
        for letter in letters:
            m = hashlib.md5()
            # im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))

            guess = []

            for image in imageset:
                for y in imageset[image]:
                    # print(y)
                    if len(y) != 0:
                        guess.append((VectorCompare.VectorCompare.relation(y, MLVector.MLVector.build_vector(letter))
                                      , image))

            print('----------next %s letter ----------' % count)
            guess.sort(reverse=True)
            for g in guess:
                print(g)

            count += 1


    # def __possible_date(self):

import os
from PIL import Image

class MLVector:

    __inconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    __imageset = {}

    def model_training(self, path):
        imageset = {}

        for letter in self.__inconset:
            temp = []

            for img in [i for i in os.listdir(path)
                        if os.path.isfile(os.path.join(path, i)) and letter in i.split(' ')[0]]:
                    # temp_path = os.path.join(path, img)
                    temp.append(MLVector.build_vector(Image.open(os.path.join(path, img))))
            # print(letter)
            imageset[letter] = temp
        self.__imageset = imageset

    @staticmethod
    def build_vector(im):
        d1 = {}
        count = 0
        temp = im.getdata()

        for i in im.getdata():
            d1[count] = i
            count += 1

        return d1

    def get_imageset(self):
        return self.__imageset
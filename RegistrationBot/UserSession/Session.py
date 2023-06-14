class Session:
    __EmbassyUrl = ''
    __UserId = 0
    __UserSd = 0
    __fullPathUrl = ''
    __Ems = ''
    __Image_path = ''
    __Logger_path = ''
    __image_ml_path = ''

    def __init__(self, config: dict):
        self.__UserId = config['bot']['id']
        self.__UserSd = config['bot']['sd']
        self.__EmbassyUrl = config['api']['base_url']
        self.__Ems = config['bot']['ems']

        if config['api']['full_path_url'] == "default":
            self.__combineFullUrl()
        else:
            self.__fullPathUrl = config['api']['full_path_url']

        self.__Image_path = config['logging']['image_path']
        self.__Logger_path = config['logging']['path']
        self.__image_ml_path = config['logging']['image_ml_path']

    def __combineFullUrl(self):
        path = "http://" \
               + self.__EmbassyUrl \
               + "/queue/OrderInfo.aspx?id=" \
               + self.__UserId \
               + "&cd=" \
               + self.__UserSd

        if self.__Ems != '':
            path = path + "&ems" \
                   + self.__Ems

        self.__fullPathUrl = path

    def GetFullUrl(self):
        return self.__fullPathUrl

    def GetImagePath(self):
        return self.__Image_path

    def GetLoggerPath(self):
        return self.__Logger_path

    def GetImageMLPath(self):
        return self.__image_ml_path

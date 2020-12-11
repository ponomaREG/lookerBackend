





class VKAPIHelpers:


    @staticmethod
    def getAvailablePhotoUrl(vkApi_response,fields):
        for key in fields:
            if(key in vkApi_response):
                return vkApi_response[key]
        return "https://www.f6s.com/images/profile-placeholder-user.jpg"
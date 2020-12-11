import threading
from datetime import datetime
import time
from app.model.SqlExecuter import SqlExecuter
from app.util.vkApiHelper import VKAPIHelpers


class lookerThread(threading.Thread):
    name = None
    vk_id = -1
    api = None
    db = None
    interval = None
    is_alive = True

    def __init__(self,name,vk_id,api,intervalInSec):
        threading.Thread.__init__(self)
        self.name = name
        self.vk_id = vk_id
        self.api = api
        self.interval = intervalInSec
        # self.db = db


    def run(self):
        while self.is_alive:
            fields = ["photo_400_orig","photo_200", "photo_100", "photo_200_orig","photo_50",  "photo_max", "photo_max_orig"]
            try:
                request = self.api.users.get(user_id=self.vk_id,fields=['online']+fields)
            except:
                time.sleep(30)
                continue
            online = request[0]['online']
            image_url = VKAPIHelpers.getAvailablePhotoUrl(request[0],fields)
            cursor = SqlExecuter.executeModification('insert into online("online","vk_id") values({},{});'.format(online,self.vk_id))
            time.sleep(self.interval)


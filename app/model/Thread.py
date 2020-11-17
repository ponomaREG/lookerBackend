import threading
from datetime import datetime
import time
from app.model.SqlExecuter import SqlExecuter


class lookerThread(threading.Thread):
    name = None
    vk_id = -1
    api = None
    db = None
    is_alive = True

    def __init__(self,name,vk_id,api):
        threading.Thread.__init__(self)
        self.name = name
        self.vk_id = vk_id
        self.api = api
        # self.db = db

    def run(self):
        while self.is_alive:
            try:
                request = self.api.users.get(user_id=self.vk_id,fields=['online'])
            except:
                time.sleep(30)
                continue
            online = request[0]['online']
            cursor = SqlExecuter.executeModification('insert into online("online","vk_id") values({},{});'.format(online,self.vk_id))
            time.sleep(5)


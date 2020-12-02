import sqlite3
from app.model.SqlExecuter import SqlExecuter
import requests
import os
from app.util.vkHolder import VKHolder
from app import app


class Data:



    @staticmethod
    def addOnlineToUser(vk_id,online):
        result = {}
        lastrowid = SqlExecuter.executeModification('insert into online("online","vk_id") values({},{});'.format(online,vk_id))
        if(lastrowid > -1):
            result['status'] = 0
            result['lastrowid'] = lastrowid 
        else:
            result['status'] = 11
        return result

    @staticmethod
    def getOnlineByVkID(vk_id,period_begin,period_end):
        result = {}
        data = SqlExecuter.getDataByQueryAll("SELECT * from online where date between '{}' and '{}' and vk_id = {};".format(period_begin,period_end,vk_id))
        if(len(data) > 0):
            result['status'] = 0
            result['data'] = data
        else:
            result['status'] = 10
        return result

    @staticmethod
    def getPersons():
        result = {}
        data = SqlExecuter.getDataByQueryAll("select DISTINCT  onl.vk_id || '.jpg'  as 'photoURL',onl.vk_id, usrs.first_name, usrs.last_name from online as onl inner join vk_users as usrs where usrs.vk_id = onl.vk_id order by onl.vk_id;")
        if(len(data) > 0):
            result['status'] = 0
            result['data'] = data
        else:
            result['status'] = 12
            result['data'] = []
        return result


    @staticmethod
    def checkIfPhotoAlreadyDownloadedAndElseDownloadIt(vk_id):
        photoname = "{}.jpg".format(vk_id)
        photopath = os.path.join(app.config['UPLOAD_FOLDER'],photoname)
        if(os.path.isfile(photopath)):
            return True
        pic_url = VKHolder.api.users.get(user_id=vk_id,fields=['photo_400_orig'])[0]['photo_400_orig']
        with open(photopath, 'wb') as handle:
            response = requests.get(pic_url, stream=True)
            if not response.ok:
                print(response)
                return False
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        return True

    @staticmethod
    def checkIfUserExistsInDatabaseAndElseInsertHim(vk_id):
        data = SqlExecuter.getDataByQueryOne("select * from vk_users where vk_id = {};".format(vk_id))
        if(data is None):
            userInfo = VKHolder.api.users.get(user_id = vk_id)
            last_name = userInfo[0]['last_name']
            first_name = userInfo[0]['first_name']
            lastrowid = SqlExecuter.executeModification('insert into vk_users values({},"{}","{}");'.format(vk_id,last_name,first_name))
            return lastrowid > -1
        return True
        

    

        

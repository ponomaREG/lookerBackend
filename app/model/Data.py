import sqlite3
from app.model.SqlExecuter import SqlExecuter
import requests
import os
from app.util.vkHolder import VKHolder
from app.util.vkApiHelper import VKAPIHelpers
from app import app
import threading


class Data:

#-----------------------------------------------------------
#USER ROUTE
#-----------------------------------------------------------

    @staticmethod
    def getUserVkInfo(vk_id):
        fields = ["photo_400_orig","photo_200", "photo_100", "photo_200_orig","photo_50",  "photo_max", "photo_max_orig"]
        userInfo = VKHolder.api.users.get(user_id = vk_id,fields=fields)
        last_name = userInfo[0]['last_name']
        first_name = userInfo[0]['first_name']
        pic_url = VKAPIHelpers.getAvailablePhotoUrl(userInfo[0],fields)
        return [{'last_name':last_name,'first_name':first_name,'imageURL':pic_url,'vk_id':str(vk_id)}]


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


#-----------------------------------------------------------
#ONLINE DATA
#-----------------------------------------------------------
    @staticmethod
    def getOnlineByVkID(vk_id,period_begin,period_end):
        result = {}
        data = SqlExecuter.getDataByQueryAll("SELECT date,online from online where date between '{}' and '{}' and vk_id = {} order by date;".format(period_begin,period_end,vk_id))
        if(len(data) > 0):
            result['status'] = 0
        else:
            result['status'] = 10
        result['data'] = data
        result['vk_id'] = vk_id
        return result

    @staticmethod
    def getOnlineByDay(vk_id,day):
        result = Data.getOnlineByVkID(vk_id,"{} 00:00:00".format(day),"{} 23:59:59".format(day))
        return resu


    
#-----------------------------------------------------------
#THREAD DATA
#-----------------------------------------------------------
    @staticmethod
    def stopThreads():
        for thread in threading.enumerate():
            if(type(thread.name) is int):
                thread.is_alive = False


    @staticmethod
    def statusThread(name):
        res = {}
        res['info'] = Data.getUserVkInfo(name)[0]
        for thread in threading.enumerate():
            if(type(thread.name) is int) and (thread.name == name):
                res['active'] = True
                return res
        res['active'] = False
        return res
                
        

    @staticmethod
    def getActiveThreads():
        res = []
        for thread in threading.enumerate():
            if(type(thread.name) is int):
                res.append(thread.name)
        return res

    @staticmethod
    def startThread(name,interval):
        for thread in threading.enumerate():
            if(thread.name == name):
                return {'status':25}
        thread = lookerThread(name,name,VKHolder.api,intervalInSec)
        thread.start()
        return {'status':0}

    @staticmethod
    def stopThread(name):
        res = []
        for thread in threading.enumerate():
            if(thread.name == name):
                thread.is_alive = False
                return {'status':0}
        return{'message':'Not found','status':3}

#-----------------------------------------------------------
#PERSONS ROUTE
#-----------------------------------------------------------
    @staticmethod
    def getPersons():
        result = {}
        data = SqlExecuter.getDataByQueryAll("select DISTINCT onl.vk_id,usrs.imageURL, usrs.first_name, usrs.last_name from online as onl inner join vk_users as usrs where usrs.vk_id = onl.vk_id order by onl.vk_id;")
        if(len(data) > 0):
            result['status'] = 0
            result['data'] = data
        else:
            result['status'] = 12
            result['data'] = []
        return result


    # @staticmethod
    # def checkIfPhotoAlreadyDownloadedAndElseDownloadIt(vk_id):
    #     photoname = "{}.jpg".format(vk_id)
    #     photopath = app.config['UPLOAD_FOLDER'] + "\\" + photoname
    #     #photopath = os.path.join(app.config['UPLOAD_FOLDER'],photoname)
    #     if(os.path.isfile(photopath)):
    #         return True
    #     pic_url = VKHolder.api.users.get(user_id=vk_id,fields=['photo_400_orig'])[0]['photo_400_orig']
    #     with open(photopath, 'wb') as handle:
    #         response = requests.get(pic_url, stream=True)
    #         if not response.ok:
    #             print(response)
    #             return False
    #         for block in response.iter_content(1024):
    #             if not block:
    #                 break
    #             handle.write(block)
    #     return True


#-----------------------------------------------------------
#ANOTHER DATA
#-----------------------------------------------------------


    @staticmethod
    def checkIfUserExistsInDatabaseAndElseInsertHim(vk_id):
        data = SqlExecuter.getDataByQueryOne("select * from vk_users where vk_id = {};".format(vk_id))
        if(data is None):
            userInfo = VKHolder.api.users.get(user_id = vk_id)
            last_name = userInfo[0]['last_name']
            first_name = userInfo[0]['first_name']
            pic_url = VKHolder.api.users.get(user_id=vk_id,fields=['photo_400_orig'])[0]['photo_400_orig']
            lastrowid = SqlExecuter.executeModification('insert into vk_users values({},"{}","{}","{}");'.format(vk_id,last_name,first_name,pic_url))
            return lastrowid > -1
        return True
        

    

        

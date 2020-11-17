import sqlite3
from app.model.SqlExecuter import SqlExecuter


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

    

        

from app import app
from flask import jsonify,request
from app.model.Data import Data
from app.model.Thread import lookerThread
from app.util.noneChecker import isArgsNone
import threading
from app.util.vkHolder import VKHolder

@app.route('/add',methods=['GET'])
def addOnline():
    result = {}
    online = request.args.get('online',type=int)
    vk_id = request.args.get('vk_id',type=int)
    if(isArgsNone(online,vk_id)):
        result['status'] = 2
        result['message'] = 'Not enough arguments'
        return jsonify(result)
    # user id
    result = Data.addOnlineToUser(vk_id,online)
    return jsonify(result)


@app.route('/persons',methods=['GET'])
def getPersons():
    result = Data.getPersons()
    return result

@app.route('/test',methods = ['GET'])
def test():
    return jsonify({"status":0,"method":"Test123"})


@app.route('/thread/active',methods=['GET'])
def getActiveThreads():
    res = []
    for thread in threading.enumerate():
        if(type(thread.name) is int):
            res.append(thread.name)
    return jsonify({'status':0,'res':res})

@app.route('/get/period',methods=['GET'])
def getOnlineByPeriod():
    result = {}
    vk_id = request.args.get('vk_id',type = int)
    period_begin = request.args.get('period_begin',type=str)
    period_end = request.args.get('period_end',type=str)
    if(isArgsNone(vk_id,period_begin,period_end)):
        result['status'] = 2
        result['message'] = 'Not enough arguments'
        return jsonify(result)
    result = Data.getOnlineByVkID(vk_id,period_begin,period_end)
    return jsonify(result)


@app.route("/persons/info",methods=['GET'])
def getUserVkInfo():
    result = {}
    vk_id = request.args.get('vk_id',type=int)
    if(isArgsNone(vk_id)):
        result['status'] = 2
        result['message'] = 'Not enough arguments'
        return jsonify(result)
    data = Data.getUserVkInfo(vk_id)
    result['data'] = data
    result['status'] = 0
    return jsonify(result)


@app.route('/persons/add')
def addNewPerson():
    result= {}
    vk_id = request.args.get("vk_id",type=int)
    if(isArgsNone(vk_id)):
        result['status'] = 2
        result['message'] = 'Not enough arguments'
        return jsonify(result)
    return testThread(vk_id)
    


@app.route('/get/day',methods=["GET"])
def getOnlibeByDay():
    result = {}
    vk_id = request.args.get('vk_id',type=int)
    day = request.args.get('day',type=str)
    if(isArgsNone(vk_id,day)):
        result['status'] = 2
        result['message'] = 'Not enough arguments'
        return jsonify(result)
    result = Data.getOnlineByDay(vk_id,day)
    return jsonify(result)


@app.route('/thread/<int:name>/start',methods=['GET'])
def testThread(name):
    # if(not Data.checkIfPhotoAlreadyDownloadedAndElseDownloadIt(name)):
    #     return jsonify({'status':20})
    intervalInSec = request.args.get('interval',type=int,default=5)
    if(not Data.checkIfUserExistsInDatabaseAndElseInsertHim(name)):
        return jsonify({"status":21})
    thread = lookerThread(name,name,VKHolder.api,intervalInSec)
    thread.start()
    return jsonify({'status':0})
    
@app.route('/thread/<int:name>/stop')
def stopThread(name):
    res = []
    for thread in threading.enumerate():
        if(thread.name == name):
            thread.is_alive = False
            return jsonify({'status':0})
    return jsonify({'status':5,'message':'Not found this thread'}) 


@app.route('/thread/stop',methods=['GET'])
def stopAllThreads():
    for thread in threading.enumerate():
        if(type(thread.name) is int):
            thread.is_alive = False
    return jsonify({'status':0})


@app.route('/thread/get',methods = ['GET'])
def getAllThreads():
    res = []
    for thread in threading.enumerate():
        res.append(thread.name)
    return jsonify({'res':res,'status':0})

    
@app.errorhandler(404)
def error404handler(e):
    return jsonify({'status':3,'message':'Not found this method'})

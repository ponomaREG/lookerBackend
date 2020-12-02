import sqlite3
from app import app

db = sqlite3.connect(app.config['DB_PATH'],check_same_thread=False)


class SqlExecuter:

    @staticmethod
    def __prepareData(allRows,columns):
        result = []
        for row in allRows:
            data = {}
            result.append(SqlExecuter.__prepareDataOneRow(row,columns))
        return result

    @staticmethod
    def __prepareDataOneRow(oneRow,columns):
        i = 0
        result = {}
        for column in columns:
            result[column] = oneRow[i]
            i+=1
        return result

    @staticmethod
    def executeModification(query):
        cursor = db.execute(query)
        lastrowid = cursor.lastrowid
        cursor.close()
        db.commit()
        return lastrowid

    @staticmethod
    def getDataByQueryAll(query):
        cursor = db.execute(query)
        columns = [description[0] for description in cursor.description]
        allRows = cursor.fetchall()
        cursor.close()
        return SqlExecuter.__prepareData(allRows,columns)

    @staticmethod
    def getDataByQueryOne(query):
        cursor = db.execute(query)
        columns = [description[0] for description in cursor.description]
        oneRow = cursor.fetchone()
        cursor.close()
        if(oneRow is None):
            return None
        return SqlExecuter.__prepareDataOneRow(oneRow,columns)


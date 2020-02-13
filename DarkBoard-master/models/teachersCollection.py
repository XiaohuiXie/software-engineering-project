from DarkBoard.models.userCollection import userCollection

import sys
class teachersCollection(userCollection):

    def __init__(self, db):
        super().__init__()
        self.collection = db.db.Teachers
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])
        if self.curMaxID == None:
            self.curMaxID = 70000000-1
        else:
            self.curMaxID = self.curMaxID["ID"]

    def create(self, name):
        self.curMaxID += 1
        self.collection.insert({
            "ID":self.curMaxID,
            "Name":name,
            "Classes":[]
        })
        return self.curMaxID

    def addClass(self, teacherID, classID):
        if self.collection.find({"ID":int(teacherID)}):
            self.collection.update_one({"ID":int(teacherID)},
                                   {"$addToSet": {"Classes": int(classID)}}
                                   , upsert=False)
            return 0
        return 1

    def removeClass(self, teacherID, classID):
        if self.collection.find({"ID":int(teacherID)}):
            self.collection.update_one({"ID":int(teacherID)},
                                   {"$pull": {"Classes": classID}}
                                   , upsert=False)
            return 0
        return 1

    def getClasses(self, teacherID):
        res = self.collection.find({"ID":int(teacherID)})
        return res.next()["Classes"]

    def hasClass(self, teacherID, classID):
        res = self.collection.find({"ID":int(teacherID)})
        return int(classID) in res.next()["Classes"]
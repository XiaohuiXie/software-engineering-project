from DarkBoard.models.userCollection import userCollection

class studentsCollection(userCollection):

    def __init__(self, db):
        super().__init__()
        self.collection = db.db.Students
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])
        if self.curMaxID == None:
            self.curMaxID = 90000000-1
        else:
            self.curMaxID = self.curMaxID["ID"]


    def create(self, name):
        self.curMaxID += 1
        self.collection.insert({
            "ID":self.curMaxID,
            "Name":name,
            "Classes":[],
            "Phone":""
        })
        return self.curMaxID

    def addClass(self, studentID, classID):
        if self.collection.find({"ID":int(studentID)}):
            self.collection.update_one({"ID":int(studentID)},
                                   {"$addToSet": {"Classes": classID}}
                                   , upsert=False)
            return 0
        return 1

    def getClasses(self, studentID):
        res = self.collection.find({"ID": int(studentID)})
        return res.next()["Classes"]


    def hasClass(self, studentID, classID):
        res = self.collection.find({"ID":int(studentID)})
        return int(classID) in res.next()["Classes"]
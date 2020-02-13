import sys

class userCollection:
    def __init__(self):
        pass

    def create(self, name):
        self.curMaxID += 1
        self.collection.insert({
            "ID":self.curMaxID,
            "Name":name,
            "Phone": ""
        })
        return self.curMaxID

    def getName(self, ID):
        res = self.collection.find({"ID": ID})
        if res.count() == 1:
            information = res.next()
            return information["Name"]
        else:
            return 0

    def delete(self, ID):
        if self.collection.find({"ID":ID}):
            self.collection.remove({"ID":ID})
            return 0
        return 1

    def setNumber(self, ID, phone):
        if self.collection.find({"ID":ID}):
            self.collection.update({"ID":ID},
                                       {"$set":{"Phone":phone}})
            return 0
        return 1

    def getNumber(self, ID):
        res = self.collection.find({"ID": ID})
        if res.count() == 1:
            information = res.next()
            return information["Phone"]
        else:
            return 0
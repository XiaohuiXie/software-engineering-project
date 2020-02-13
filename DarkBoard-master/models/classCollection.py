import sys
class classesCollection:

    def __init__(self, db):
        super().__init__()
        self.collection = db.db.Classes
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])
        if self.curMaxID == None:
            self.curMaxID = 1000000-1
        else:
            self.curMaxID = self.curMaxID["ID"]

    def create(self, name, teacherID, location, days, startTime, endTime):
        dayString = ""
        for d in days:
            dayString += d
        self.curMaxID += 1
        self.collection.insert({
            "ID": self.curMaxID,
            "Name": name,
            "Teacher": int(teacherID),
            "Locations": location ,
            "Times": dayString + " " + startTime + "-" + endTime,
            "Assignments": [],
            "GradeScheme" : [],
            "Announcements":[],
            "Students" : [],

        })
        return self.curMaxID

    def getName(self, ID):
        res = self.collection.find({"ID": int(ID)})
        if res.count() == 1:
            information = res.next()
            return information["Name"]
        else:
            return 0

    def getLocations(self, ID):
        res = self.collection.find({"ID": int(ID)})
        if res.count() == 1:
            information = res.next()
            return information["Locations"]
        else:
            return 0

    def getTimes(self, ID):
        res = self.collection.find({"ID": int(ID)})
        if res.count() == 1:
            information = res.next()
            return information["Times"]
        else:
            return 0

    def getTeacher(self, ID):
        res = self.collection.find({"ID": int(ID)})
        if res.count() == 1:
            information = res.next()
            return information["Teacher"]
        else:
            return 0

    def delete(self, ID):
        if self.collection.find({"ID": ID}).count() == 1:
            self.collection.remove({"ID": ID})
            return 0
        return 1

    def hasAssignment(self, cID, assignmentID):
        return int(assignmentID) in self.collection.find({"ID":int(cID)}).next()["Assignments"]

    def addAssignment(self, classID, assignmentID):
        self.collection.update({"ID": int(classID)}, {"$addToSet" : {"Assignments" : assignmentID}})

    def getAssignments(self, classID):
        return self.collection.find({"ID":int(classID)}).next()["Assignments"]

    def defineAssignmentType(self, classID, typeID, numberLowestToDrop, value):
        value = int(value) / 100
        self.collection.update({"ID" : int(classID)}, {"$addToSet" : {"GradeScheme" :{typeID : value, "NumberOfLowestToDrop" : int(numberLowestToDrop)}}})

    def removeAssignment(self, classID, assignmentID):
        self.collection.update({"ID" :int(classID)}, {"$pull" : {"Assignments" : int(assignmentID)}})

    def addAnnouncement(self, classID, announcement):
        self.collection.update({"ID": int(classID)}, {"$addToSet" : {"Announcements" : announcement}})

    def getAnnouncements(self, classID):
        return self.collection.find({"ID":int(classID)}).next()["Announcements"]

    def addStudent(self, classID, studentID):
        self.collection.update({"ID": int(classID)}, {"$addToSet" : {"Students" : int(studentID)}})

    def getStudents(self, classID):
        return self.collection.find({"ID":int(classID)}).next()["Students"]

    def getGradeScheme(self, classID):
        return self.collection.find({"ID":int(classID)}).next()["GradingScheme"]
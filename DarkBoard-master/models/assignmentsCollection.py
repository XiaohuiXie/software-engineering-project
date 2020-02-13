import sys
'''
Assignments collection

{
    ID: int,
    Name: str,
    Description: str,
    DueTime: str,
    DueDate: str,
    Type: str
}
'''
class assignmentsCollection:

    def __init__(self, db):
        super().__init__()
        self.collection = db.db.Assignments
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])
        if self.curMaxID == None:
            self.curMaxID = 100000000-1
        else:
            self.curMaxID = self.curMaxID["ID"]

    '''
    Creates assignment
    '''
    def create(self, name, description, type, dueDate, dueTime):

        self.curMaxID += 1
        self.collection.insert({
            "ID": self.curMaxID,
            "Name": name,
            "Description": description,
            "DueTime": dueTime,
            "DueDate": dueDate,
            "Type": type,
            "Grades": {},
            "DiscrepFlag": {},
            "TeacherComment": {},
            "StudentComment": {}
        })
        return self.curMaxID

    def editAssignment(self, assignmentID, name, description, aType, dueDate, dueTime):
        self.collection.update(
            {"ID": int(assignmentID)},
            {
                "$set":
                    {
                        "Name": name,
                        "Description": description,
                        "DueTime": dueTime,
                        "DueDate": dueDate,
                        "Type": aType,
                        "Grades": {},
                        "DiscrepFlag": {},
                        "TeacherComment": {},
                        "StudentComment": {}
                    }
            }
        )

    def getAll(self, ID):
        res = self.collection.find({"ID": int(ID)})
        if res.count() == 1:
            information = res.next()
            return information
        else:
            return 0

    def getAttrib(self, ID, attrib):
        res = self.collection.find({"ID": int(ID)})
        if res.count() == 1:
            information = res.next()
            return information[attrib]
        else:
            return 0

    def getName(self, ID):
        return self.getAttrib(ID, "Name")

    def getDescription(self, ID):
        return self.getAttrib(ID, "Description")

    def getDueTime(self, ID):
        return self.getAttrib(ID, "DueTime")

    def getDueDate(self, ID):
        return self.getAttrib(ID, "DueDate")

    def getType(self, ID):
        return self.getAttrib(ID, "Type")

    def delete(self, ID):
        if self.collection.find({"ID": int(ID)}).count() == 1:
            self.collection.remove({"ID": int(ID)})
            return 0
        return 1

    def grade(self, aID, sID, grade):
        path = "Grades." + str(sID)
        res = self.collection.find({
            "ID": int(aID)
        })
        if grade != "Ungraded" and grade != "Not Graded":
            grade = int(grade)
        if res.count() == 1:
            self.collection.update({
                "ID": int(aID)
            },{"$set": {path : grade}}, upsert=True)
        return ''

    def getGrade(self, aID, sID):
        res = self.collection.find({
            "ID": int(aID)
        })
        grade = res.next()["Grades"].get(str(sID), None)
        if grade != None:
            return grade
        return -1

    def setDiscrepFlag(self, aID, sID, flag):
        path = "DiscrepFlag." + str(sID)
        res = self.collection.find({
            "ID": int(aID)
        })
        if flag:
            value = 1
        else:
            value = 0
        if res.count() == 1:
            self.collection.update({
                "ID": int(aID)
            },{"$set": {path : value}}, upsert=True)
            return True
        return False

    def getDiscrepFlag(self, aID, sID):
        res = self.collection.find({
            "ID": int(aID)
        })
        flag = res.next()["DiscrepFlag"].get(str(sID), 0) == 1
        print(flag, file=sys.stderr)
        return flag

    def setTeacherComment(self, aID, sID, comment):
        path = "TeacherComment." + str(sID)
        res = self.collection.find({
            "ID": int(aID)
        })
        if len(comment) > 200:
            comment = comment[:200]
        if res.count() == 1:
            self.collection.update({
                "ID": int(aID)
            },{"$set": {path : comment}}, upsert=True)
            return True
        return False

    def getTeacherComment(self, aID, sID):
        res = self.collection.find({
            "ID": int(aID)
        })
        flag = res.next()["TeacherComment"].get(str(sID), "")
        return flag


    def setStudentComment(self, aID, sID, comment):
        path = "StudentComment." + str(sID)
        res = self.collection.find({
            "ID": int(aID)
        })
        if len(comment) > 200:
            comment = comment[:200]
        if res.count() == 1:
            self.collection.update({
                "ID": int(aID)
            },{"$set": {path : comment}}, upsert=True)
            return True
        return False

    def getStudentComment(self, aID, sID):
        res = self.collection.find({
            "ID": int(aID)
        })
        flag = res.next()["StudentComment"].get(str(sID), "")
        return flag
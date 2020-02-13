from flask_pymongo import PyMongo
from DarkBoard.models.adminsCollection import adminsCollection
from DarkBoard.models.studentsCollection import studentsCollection
from DarkBoard.models.teachersCollection import teachersCollection
from DarkBoard.models.loginsCollection import loginsCollection
from DarkBoard.models.classCollection import classesCollection
from DarkBoard.models.assignmentsCollection import assignmentsCollection
from twilio.rest import Client

account_sid = 'AC9b661c29027fa262cd1362590d1e44aa'
auth_token = '69288769a2a0bbe5416999d1b74e19ac'

'''
This is the interface to the Backend functionality, connecting the backend components
into one centralized place.

!Only interact with the backend through this interface!

To use the Backend object do not create one in your script instead use,
form app import app, Backend
'''
class Backend:

    def __init__(self, db):
        self.adminsCollection = adminsCollection(db)
        self.teachersCollection = teachersCollection(db)
        self.studentsCollection = studentsCollection(db)
        self.loginsCollection = loginsCollection(db)
        self.classesCollection = classesCollection(db)
        self.assignmentsCollection = assignmentsCollection(db)

    '''
    Create a user account
    
    :param name, the name of the user for display purposes ie Matthew Schofield
    :param username, for authentication purposes
    :param hashedPassword, for authentication purposes
    :param accountType, to understand permissions of an account
    '''
    def createAccount(self, name, username, hashedPassword, accountType):
        if accountType == "admin":
            ID = self.adminsCollection.create(name)
        elif accountType == "student":
            ID = self.studentsCollection.create(name)
        elif accountType == "teacher":
            ID = self.teachersCollection.create(name)
        else:
            # Error
            ID = -1
        return self.loginsCollection.create(username, hashedPassword, ID)

    def deleteAccount(self, ID):
        ID = int(ID)
        if ID == 10000000:
            return 1
        else:
            self.loginsCollection.delete(ID)
            if ID > 10000000 and ID < 20000000:
                return self.adminsCollection.delete(ID)
            elif ID >= 70000000 and ID < 80000000:
                return self.teachersCollection.delete(ID)
            elif ID >= 90000000 and ID < 100000000:
                return self.studentsCollection.delete(ID)

    def createClass(self, name, teacherID, location, days, startTime, endTime):
        classID = self.classesCollection.create(name, teacherID, location, days, startTime, endTime)
        if classID > 0:
            self.teachersCollection.addClass(teacherID, classID)

    def addStudentToClass(self, classID, studentID):
        self.studentsCollection.addClass(studentID, classID)
        self.classesCollection.addStudent(classID, studentID)

    def deleteClass(self, ID):
        teachers = self.classesCollection.getTeacher(int(ID))
        self.teachersCollection.removeClass(teachers, int(ID))
        return self.classesCollection.delete(int(ID))

    def getName(self,ID):
        ID = int(ID)
        if ID >= 10000000 and ID < 20000000:
            return self.adminsCollection.getName(ID)
        elif ID >= 70000000 and ID < 80000000:
            return self.teachersCollection.getName(ID)
        elif ID >= 90000000 and ID < 100000000:
            return self.studentsCollection.getName(ID)

    def getClassName(self, ID):
        return self.classesCollection.getName(ID)


    def getClassTeacher(self, ID):
        return self.classesCollection.getTeacher(ID)

    def getClassLocations(self, ID):
        return self.classesCollection.getLocations(ID)

    '''
    Get the times of a class
    
    ID - int ID of the class whose times are to be obtained
    '''
    def getClassTimes(self, ID):
        return self.classesCollection.getTimes(ID)

    '''
    Get a list of Teacher's classes
    
    ID - int ID of the teacher whose classes to get
    '''
    def getTeacherClasses(self, ID):
        return self.teachersCollection.getClasses(ID)

    '''
    Get a list of Teacher's classes

    ID - int ID of the teacher whose classes to get
    '''

    def getStudentClasses(self, ID):
        return self.studentsCollection.getClasses(ID)

    '''
    Updates the password of a User
    !No checks simply does so!
    ID - int ID of User whose password is to be updated
    newPass - new password (already hashed)    
    '''
    def updatePassword(self, ID, newPass):
        self.loginsCollection.updatePassword(ID,newPass)

    '''
    Removes the login block from a User's account
    
    ID - int ID of user whose login block should be removed
    '''
    def clearBlock(self, ID):
        self.loginsCollection.clearBlock(ID)

    def checkTeacherHasClass(self, tID, cID):
        return self.teachersCollection.hasClass(tID, cID)


    def checkStudentHasClass(self, sID, cID):
        return self.studentsCollection.hasClass(sID, cID)

    def classHasAssignment(self, cID, aID):
        return self.classesCollection.hasAssignment(cID, aID)

    def defineAssignmentType(self, classID, typeID, numberLowestToDrop, value):
        self.classesCollection.defineAssignmentType(classID, typeID, numberLowestToDrop, value)

    def createAssignment(self, classID, name, description, type, dueDate, dueTime):
        assignmentID = self.assignmentsCollection.create(name, description, type, dueDate, dueTime)
        if assignmentID != -1:
            self.classesCollection.addAssignment(classID, assignmentID)

    def deleteAssignment(self, uID, classID, assignmentID):
        if self.checkTeacherHasClass(uID, classID) and self.classHasAssignment(classID, assignmentID):
            self.classesCollection.removeAssignment(classID, assignmentID)
            self.assignmentsCollection.delete(assignmentID)
            return '', 204
        else:
            return '', 403

    def getClassAssignments(self, classID):
        return self.classesCollection.getAssignments(int(classID))

    def getAssignmentInfo(self, assignmentID):
        return self.assignmentsCollection.getAll(int(assignmentID))

    def addAnnouncementToClass(self, classID, announcement):
        return self.classesCollection.addAnnouncement(classID, announcement)

    def getAnnouncementsForClass(self, classID):
        return self.classesCollection.getAnnouncements(classID)

    def editAssignment(self, uID, classID, assignmentID, name, description, aType, dueDate, dueTime):
        if self.checkTeacherHasClass(uID, classID) and self.classHasAssignment(classID, assignmentID):
            self.assignmentsCollection.editAssignment(assignmentID, name, description, aType, dueDate, dueTime)
            return '', 204
        else:
            return '', 403

    def getStudentsForClass(self, cID):
        return self.classesCollection.getStudents(cID)

    def gradeAssignment(self, aID, studentID, grade):
        return self.assignmentsCollection.grade(aID, studentID, grade)

    def getGrade(self, aID, studentID):
        return self.assignmentsCollection.getGrade(aID, studentID)

    def getFinalGrade(self, cID, sID):
        return 100

    def setDiscrepFlag(self, aID, sID, flag):
        self.assignmentsCollection.setDiscrepFlag(aID, sID, flag)
        return '', 403

    def getDiscrepFlag(self, aID, sID):
        return self.assignmentsCollection.getDiscrepFlag(aID, sID)

    def setTeacherComment(self, aID, sID, comment):
        self.assignmentsCollection.setTeacherComment(aID, sID, comment)
        return '', 403

    def getTeacherComment(self, aID, sID):
        return self.assignmentsCollection.getTeacherComment(aID, sID)

    def setStudentComment(self, aID, sID, comment):
        self.assignmentsCollection.setStudentComment(aID, sID, comment)
        return '', 403

    def getStudentComment(self, aID, sID):
        return self.assignmentsCollection.getStudentComment(aID, sID)

    def setStudentNumber(self, sID, phoneNumber):
        self.studentsCollection.setNumber(sID, phoneNumber)

    def getStudentNumber(self, sID):
        return self.studentsCollection.getNumber(sID)

    def sendOutNotifications(self, cID, name):
        client = Client(account_sid, auth_token)
        for student in self.getStudentsForClass(cID):
            numb = self.getStudentNumber(student)
            if numb != "":
                numb = "+1"+numb
                message = client.messages.create(
                body = "New Assignment " + str(name),
                from_ = '+18572738052',
                to = numb)
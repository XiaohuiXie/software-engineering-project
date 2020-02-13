'''
The main routes for flask,
This is to answer user requests and to primarily rely on
the Backend for most logic and database communication
'''
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from DarkBoard.backend import Backend
from DarkBoard.pagebuilder import PageBuilder
from DarkBoard import db
from DarkBoard.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import json
from statistics import stdev, median, mean

# Backend object to handle most logic and database communications
Backend = Backend(db)
pageBuilder = PageBuilder()

# Register itself as the main route
main = Blueprint('main', __name__)


'''
Responds with the index, a login page
'''
@main.route('/')
def index():
    if current_user != None and current_user.is_authenticated:
        if current_user.isTeacher():
            return redirect(url_for("main.teacherHomepage"))
        elif current_user.isStudent():
            return redirect(url_for("main.studentHomepage"))
        else:
            return redirect(url_for("main.adminHomepage"))


    return render_template('index.html')

'''
Admin Homepage
'''
@main.route('/adminHomepage')
@login_required
def adminHomepage():

    pageData = {}

    if current_user.attempts >= 3:
        pageData["attempts"] = current_user.attempts
        db.db.Logins.update({"ID": current_user.id}, {"$set": {"attempts": 0}})
    return render_template('adminHomepage.html', pageData=pageData)

'''
Student Homepage
'''
@main.route('/studentHomepage')
@login_required
def studentHomepage():
    pageData = {
    }

    classIDs = Backend.getStudentClasses(current_user.id)
    classes = []
    for cID in classIDs:
        classes.append(
            {
                "Name": Backend.getClassName(cID),
                "Time": Backend.getClassTimes(cID),
                "Location": Backend.getClassLocations(cID),
                "ClassID": cID,
                "Teacher": Backend.getName(Backend.getClassTeacher(cID)),
                "FinalGrade": Backend.getFinalGrade(cID, current_user.id)
            }
        )

    pageData["Classes"] = classes

    if current_user.attempts >= 3:
        pageData["attempts"] = current_user.attempts
        db.db.Logins.update({"ID": current_user.id}, {"$set": {"attempts": 0}})
    return render_template('studentHomepage.html', pageData=pageData)

'''
Teacher Homepage
'''
@main.route('/teacherHomepage')
@login_required
def teacherHomepage():
    classIDs = Backend.getTeacherClasses(current_user.id)
    classes = []
    for cID in classIDs:
        classes.append(
            {
                "Name" : Backend.getClassName(cID),
                "Time" : Backend.getClassTimes(cID),
                "Location" : Backend.getClassLocations(cID),
                "ClassID" : cID
            }
        )

    pageData = {
        "Classes" : classes
    }

    if current_user.attempts >= 3:
        pageData["attempts"] = current_user.attempts
        db.db.Logins.update({"ID": current_user.id}, {"$set": {"attempts": 0}})

    return render_template('teacherHomepage.html', pageData=pageData)

'''
Teacher's Class Homepage
'''
@main.route('/classHomepageTeacher',  methods=['GET'])
@login_required
def classHomepageTeacher():
    cID = int(request.args.get("classID"))

    if Backend.checkTeacherHasClass(current_user.id, cID):
        assignments = []
        for assignmentID in Backend.getClassAssignments(cID):
            assignments.append(
                Backend.getAssignmentInfo(assignmentID)
            )
        students = []
        grades= []
        for studentID in Backend.getStudentsForClass(cID):
            grade = Backend.getFinalGrade(cID, studentID)
            students.append(
                {
                    "StudentID":studentID,
                    "StudentName": Backend.getName(studentID),
                    "StudentGrade": grade if grade != -1 else "-"
                }
            )
            if grade > -1:
                grades.append(grade)

        pageData = {
            "ClassID" : cID,
            "Name" : Backend.getClassName(cID),
            "Time" : Backend.getClassTimes(cID),
            "Location" : Backend.getClassLocations(cID),
            "Assignments" : assignments,
            "Announcements": Backend.getAnnouncementsForClass(cID),
            "Students": students
        }

        n = len(grades)
        if n > 1:
            pageData["Mean"] = str("%.3f" % mean(grades))
            pageData["SD"] = str("%.3f" % stdev(grades))
            pageData["Median"] = median(grades)
        else:
            pageData["Mean"] = "-"
            pageData["SD"] = "-"
            pageData["Median"] = "-"
        return render_template('classHomepageTeacher.html', pageData=pageData)
    else:
        return '', 403

'''
Teacher's Class Homepage
'''
@main.route('/classHomepageStudent',  methods=['GET'])
@login_required
def classHomepageStudent():
    cID = int(request.args.get("classID"))

    if Backend.checkStudentHasClass(current_user.id, cID):
        assignments = []
        for assignmentID in Backend.getClassAssignments(cID):
            assignments.append(
                Backend.getAssignmentInfo(assignmentID)
            )

        pageData = {
            "ClassID" : cID,
            "Name" : Backend.getClassName(cID),
            "Time" : Backend.getClassTimes(cID),
            "Location" : Backend.getClassLocations(cID),
            "Assignments" : assignments,
            "Announcements": Backend.getAnnouncementsForClass(cID),
            "CurrentFinalGrade": Backend.getFinalGrade(cID, current_user.id)
        }
        return render_template('classHomepageStudent.html', pageData=pageData)
    else:
        return '', 403


'''
Command:
Creates a class given a
name
ID
startTime
endTime
location
days
'''
@main.route('/createClass', methods=['POST'])
def createClass():
    # Get form data
    name = request.form.get("name")
    ID = request.form.get("ID")
    startTime = request.form.get("timeStart")
    endTime = request.form.get("timeEnd")
    location = request.form.get("location")
    days = []
    for day in ["M","T","W","R","F"]:
        if request.form.get(day) != None:
            days.append(day)
    Backend.createClass(name, ID, location, days, startTime, endTime)
    return redirect(url_for("main.adminHomepage"), code=204)

'''
Command:
Deletes a class given a
name
ID
'''
@main.route('/deleteClass', methods=['POST'])
def deleteClass():
    # Get form data
    ID = request.form.get("ID")
    Backend.deleteClass(ID)
    return redirect(url_for("main.adminHomepage"), code=204)

'''
Settings Page
'''
@main.route('/settings')
@login_required
def settings():
    pageData = {}
    pageData["Number"] = Backend.getStudentNumber(int(current_user.id))
    return render_template("settings.html", pageData=pageData)


'''
Command:
Update a user's password given:
old password
new password
'''
@main.route('/updatePassword', methods=['POST'])
@login_required
def updatePassword():
    newHashedPassword = generate_password_hash(request.form.get("newPassword"), method='sha256')
    oldPassword = request.form.get("currentPassword")
    if check_password_hash(current_user.password, oldPassword):
        Backend.updatePassword(current_user.id, newHashedPassword)
    return redirect(url_for("main.settings"))

'''
Command:
Removes the block from a User's account

ID - ID of user to clear

:return 204 - success, no matter if the block was cleared the command executes
'''
@main.route('/clearBlock', methods=['POST'])
@login_required
def clearBlock():
    # Get form data
    ID = request.form.get("ID")
    Backend.clearBlock(ID)
    return redirect(url_for("main.adminHomepage"))

'''
Defines/Creates an assignment type given the form data:
classID
typeName - name of new assignment type
value - percent value of assignment type
numberOfLowestToDrop - drops this number of lowest grades of this type before 
        calculating

:return 204 success or 403 access denied
'''
@main.route('/defineType', methods=['POST'])
@login_required
def defineAssignmentType():
    classID = request.form.get("classID")
    if Backend.checkTeacherHasClass(current_user.id, classID):
        typeName = request.form.get("typeName")
        value = request.form.get("value")
        numberLowestToDrop = request.form.get("numberOfLowestToDrop")
        Backend.defineAssignmentType(classID, typeName, numberLowestToDrop, value)
        return redirect(url_for("main.teacherHomepage"))
    else:
        return '', 403

'''
Creates an assignment from given form data

Form data:
classID - ID of the class to add to
name - assignment name
description - description of assignment
dueDate 
dueTime
aType - assignment type

:return 204 - success or 403 access denied
'''
@main.route('/createAssignment', methods=['POST'])
@login_required
def createAssignment():
    classID = request.form.get("classID")
    if Backend.checkTeacherHasClass(current_user.id, classID):
        name = request.form.get("name")
        description = request.form.get("description")
        dueDate = request.form.get("dueDate")
        dueTime = request.form.get("dueTime")
        aType = request.form.get("type")
        Backend.createAssignment(classID, name, description, aType, dueDate, dueTime)
        Backend.sendOutNotifications(classID, name)
        return redirect(url_for("main.teacherHomepage"))
    else:
        return '', 403

'''
Edits an assignment from given form data

Form data:
classID - ID of the class to add to
name - assignment name
description - description of assignment
dueDate 
dueTime
aType - assignment type

:return 204 - success or 403 access denied
'''
@main.route('/editAssignment', methods=['POST'])
@login_required
def editAssignment():
    classID = request.form.get("classID")
    if Backend.checkTeacherHasClass(current_user.id, classID):
        assignmentID = request.form.get("assignmentID")
        name = request.form.get("name")
        description = request.form.get("description")
        dueDate = request.form.get("dueDate")
        dueTime = request.form.get("dueTime")
        aType = request.form.get("type")
        Backend.editAssignment(current_user.id, classID, assignmentID, name, description, aType, dueDate, dueTime)
        return redirect(url_for("main.assignmentPageTeacher",  classID=classID, assignmentID=assignmentID))
    else:
        return '', 403

'''
Shows the assignment page for a teacher

Recieves the form data:
classID: class with assignment
assignmentID: assignment of interest

:return html page or error code 403 access denied
'''
@main.route('/assignmentPageTeacher', methods=['GET'])
@login_required
def assignmentPageTeacher():
    cID = request.args.get("classID")
    aID = request.args.get("assignmentID")
    if Backend.checkTeacherHasClass(current_user.id, cID) and Backend.classHasAssignment(cID, aID):
        pageData = Backend.getAssignmentInfo(aID)
        pageData["ClassID"] = cID
        students = []
        grades = []
        for student in Backend.getStudentsForClass(cID):
            curGrade = Backend.getGrade(aID, student)
            if type(curGrade) is str:
                curGrade = -1
            if curGrade < 0:
                curGrade = "Not Graded"
            else:
                grades.append(curGrade)

            temp = {
                "ID": student,
                "Name":Backend.getName(student),
                "CurrentGrade": curGrade,
                "GradeDiscrep": Backend.getDiscrepFlag(aID, student),
                "CurrentComment": Backend.getTeacherComment(aID, student),
                "Student Comment": Backend.getStudentComment(aID, student)
            }
            students.append(temp)
        pageData["Students"] = students
        n = len(grades)
        if n > 1:
            pageData["Mean"] = str("%.3f" % mean(grades))
            pageData["SD"] = str("%.3f" % stdev(grades))
            pageData["Median"] = median(grades)
        else:
            pageData["Mean"] = "-"
            pageData["SD"] = "-"
            pageData["Median"] = "-"
        pageData["Complete"] = n
        pageData["Missing"] = len(students) - n
        return render_template("assignmentPageTeacher.html", pageData=pageData)
    else:
        return '', 403


'''
Deletes assignment with given assignmentID from given class with classID

Recieves the form data:
classID: class to delete assignment from
assignmentID: assignment to delete

:returns '', <code>
    code -  204, success
            403, access denied
'''
@main.route('/deleteAssignment', methods=['POST'])
@login_required
def deleteAssignment():
    classID = request.form.get("classID")
    assignmentID = request.form.get("assignmentID")
    Backend.deleteAssignment(current_user.id, classID, assignmentID)
    return redirect(url_for("main.classHomepageTeacher",  classID=classID))

'''
Command:
Creates an announcement for a class given
announcement text
'''
@main.route('/createAnnouncement', methods=['POST'])
def createAnnouncement():
    # Get form data
    announcement = request.form.get("announcement")
    classID = request.form.get("classID")
    Backend.addAnnouncementToClass(classID, announcement)
    return redirect(url_for("main.classHomepageTeacher",  classID=classID))

@main.route('/addStudentToClass', methods=['POST'])
def addStudentToClass():
    classID = int(request.form.get("classID"))
    studentID = int(request.form.get("studentID"))
    Backend.addStudentToClass(classID,studentID)
    return redirect(url_for("main.classHomepageTeacher",  classID=classID))

@main.route('/assignmentPageStudent', methods=['GET'])
def assignmentPageStudent():
    cID = request.args.get("classID")
    aID = request.args.get("assignmentID")
    sID = current_user.id
    if Backend.checkStudentHasClass(current_user.id, cID) and Backend.classHasAssignment(cID, aID):
        pageData = Backend.getAssignmentInfo(aID)
        pageData["ClassID"] = cID
        curGrade = Backend.getGrade(aID, current_user.id)
        if curGrade == "Not Graded" or curGrade == "Ungraded":
            curGrade = -1
        if curGrade >= 0:
            pageData["Grade"] = Backend.getGrade(aID, sID)
        else:
            pageData["Grade"] = "Not Graded"
        if Backend.getDiscrepFlag(aID, sID):
            pageData["Discrep"] = "checked"
        else:
            pageData["Discrep"] = ""
        pageData["Teacher Comment"] = Backend.getTeacherComment(aID, sID)
        pageData["Student Comment"] = Backend.getStudentComment(aID, sID)
        return render_template("assignmentPageStudent.html", pageData=pageData)
    else:
        return '', 403

@main.route('/gradeAssignment', methods=['POST'])
def gradeAssignment():
    aID = int(request.form.get("assignmentID"))
    cID = int(request.form.get("classID"))
    for sID in Backend.getStudentsForClass(cID):
        grade = request.form.get(str(sID))
        Backend.gradeAssignment(aID, sID, grade)
    return redirect(url_for("main.assignmentPageTeacher",  classID=cID, assignmentID=aID))

@main.route('/setDiscrepFlag', methods=['POST'])
def setDiscrepFlag():
    aID = int(request.form.get("assignmentID"))
    sID = int(request.form.get("studentID"))
    cID = request.args.get("classID")
    flag = request.form.get("flag")
    Backend.setDiscrepFlag(aID, sID, flag)
    return redirect(url_for("assignmentPageStudent.html",  classID=cID, assignmentID=aID))

@main.route('/setTeacherComments', methods=['POST'])
def setTeacherComments():
    aID = int(request.form.get("assignmentID"))
    cID = int(request.form.get("classID"))

    for sID in Backend.getStudentsForClass(cID):
        comment = request.form.get(str(sID))
        Backend.setTeacherComment(aID, sID, comment)
    return redirect(url_for("main.assignmentPageTeacher",  classID=cID, assignmentID=aID))

@main.route('/setStudentComment', methods=['POST'])
def setStudentComment():
    aID = int(request.form.get("assignmentID"))
    sID = int(request.form.get("studentID"))
    cID = request.args.get("classID")
    comment = request.form.get("comment")
    Backend.setStudentComment(aID, sID, comment)
    return redirect(url_for("assignmentPageStudent.html",  classID=cID, assignmentID=aID))

@main.route('/setStudentNumber', methods=['POST'])
def setStudentNumber():
    phoneNumber = request.form.get("phone")
    sID = current_user.id
    Backend.setStudentNumber(sID, phoneNumber)
    return redirect(url_for("main.settings"))

@main.route('/studentAPI', methods=['POST'])
def studentAPI():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User(username)

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if check_password_hash(user.password, password):
        if user.isStudent():
            sID = user.getId()
            classIDs = Backend.getStudentClasses(sID)
            classes = []
            for cID in classIDs:
                classes.append(
                    {
                        "Name": Backend.getClassName(cID),
                        "Time": Backend.getClassTimes(cID),
                        "Location": Backend.getClassLocations(cID),
                        "ClassID": cID,
                        "Teacher": Backend.getName(Backend.getClassTeacher(cID)),
                        "FinalGrade": Backend.getFinalGrade(cID, sID)
                    }
                )
            output = {
                "Name": Backend.getName(sID),
                "Classes": classes
            }
            return json.dumps(output)


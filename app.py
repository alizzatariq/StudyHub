import os
from flask import Flask, render_template, request, make_response, session, redirect, url_for
from Classes import User, Profile,TodoList
from flask_restful import Api
from DBHandler import DataBaseHandler
from flask_restful import Api,Resource
from resources import  routes

import imghdr
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key="XYZ12345" #password
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_PATH'] = 'static'


#key
db_localhost= "localhost";
db_root= "root";
db_password= "";
db_database="studyplanner";




app = Flask(__name__)
app.secret_key="XYZ12345" #password

api=Api(app)
routes.initialize_routes(api)

def checkIsDigit(str1):
    for ch in str1:
        if ch.isdigit() == True:
            return True
    return False

def validationLogin(name1):

    if checkIsDigit(name1) == True or len(name1)<=0:
        return False
    return True


def checkUserAlreadyExist(user1):
    try:
        handler = DataBaseHandler("localhost", "root", '', "studyplanner")
        return handler.checkUserExist(user1)
    except Exception as e:
        print(str(e))


@app.route('/')
def startApp():
    return render_template("homepage.html")


@app.route('/login',methods=["GET","POST"])
def login_():  # put application's code here
    if request.method=="POST":
        email = request.form["email"]
        pwd = request.form["pwd"]
    else:
        email = request.args.get("email")
        pwd = request.args.get("pwd")

    print("email= ", email, "pwd=", pwd)


    if email == None and pwd == None:
        return render_template("login.html")

    if len(str(pwd))<8:
        str1="Invalid Password. Length should be greater than 10"
        return render_template("login.html",str1=str1,warn1=True,error=True)

    login = False

    user1 = User()
    user1.email = email
    user1.password = pwd

    flag = False
    try:
        handler = DataBaseHandler("localhost", "root", '', "studyplanner")
        flag1 = handler.checkUserExist(user1)
        print("flaf1== ",flag1)
    except Exception as e:
        print(str(e))
    else:
        if flag1 == True:
            login = True

        if login == True:
                session["uemail"] = email
                session["upwd"] = pwd
                print("session completed")
                return render_template("home.html", name="Student")
        else:
            str1 = "Invalid Credentials. User Not Exist!!!"
            return render_template("login.html", str1=str1, danger1=True,error=True)

    return render_template("loginUser.html")



@app.route('/signup',methods=["GET","POST"])
def signup_():
    error=None
    print('signupppp')
    if request.method=="POST":
        email = request.form["email"]
        nm = request.form["nm"]
        pwd1 = request.form["pwd1"]
        pwd2=request.form["pwd2"]
        acctype = request.form["acctype"]
    else:
        email = request.args.get("email")
        nm = request.args.get("nm")
        pwd1 = request.args.get("pwd1")
        pwd2 = request.args.get("pwd2")
        acctype = request.args.get("acctype")

    print(email,nm,pwd1,pwd2,acctype)
    if email == None and pwd1 == None and pwd2 == None and acctype == None and nm == None:
        return render_template("signup.html")

    if len(str(pwd1))<8 or len(str(pwd2))<8:
        print("pwd not 8")
        str1 = "Invalid Password. Length should be greater than 10"
        return render_template("signup.html", str1=str1,warn1=True,error=True)

    if pwd1!=pwd2:
        print("pwd1!=pwd2")
        str1 = "Invalid Password. Password Not Match!!! Enter again"
        return render_template("signup.html", str1=str1, danger1=True,error=True)

    user1 = User()
    user1.email = email
    user1.password = pwd1
    user1.acc_type=acctype
    user1.name=nm

    login = False

    try:
        handler = DataBaseHandler("localhost", "root", '', "studyplanner")
        flag1 = handler.checkUserExist(user1)

        print("flag11= ", flag1)
        if validationLogin(nm) == True and flag1 == False:
            login = True


        print("flag= ", flag1)

        if login == True:
            handler.addUser(user1)
            str1="Account Made SuccessFully!"
            session["uemail"] = user1.email
            session["upwd"] = user1.password
            return render_template("home.html",str1=str1,success1=True,error=True)

    except Exception as e:
        print(str(e))

    else:
        if flag1 == True:
            str1 = "User Already Exist!!!!"
            return render_template("signup.html", str1=str1, warn1=True,error=True)
        else:
            str1 = "Invalid User Name. Enter user Name Again!!!"
            return render_template("signup.html", str1=str1, danger1=True,error=True)

    return render_template("signup.html")

###################################################
################################################
#################################################

def validate_image1(stream):
    try:
        header = stream.read(512)  # 512 bytes should be enough for a header check
        stream.seek(0)  # reset stream pointer
        format = imghdr.what(None, header)
        if not format:
            return None
        print("Validating")
        return '.' + (format if format != 'jpeg' else 'jpg')
    except Exception as e:
        print("Exception in validating image")

@app.route("/uploadfile", methods=['GET','POST'])
def index1():
    try:
        print("in index--1")
        files = os.listdir("static/files")
        return render_template('noteindex.html', files=files)
    except Exception as e:
        print("Exception in uploading file", str(e))
        return "Hello world"


@app.route("/uploadfile2", methods=['GET','POST'])
def upload_files1():
    print("in upload_files--2")
    uploaded_file = request.files['file']
    print("1")
    filename = secure_filename(uploaded_file.filename)
    print(filename)

    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion = ", email1, pwd1)
        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)
        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1, "")
        print(user1)
        userId = DBObj.getId(user1)
        print("User id is : ", userId)

        myfile=filename
        list1=uploaded_file.save(os.path.join("static/files", filename))


        if filename != '' and filename!=None :
            print("3")
            file_ext = os.path.splitext(filename)[1]

        return render_template("notes.html",fileNotes=myfile,fileNotes1=True, str1="Error!! Failure in setting Profile picture!", error=True,
                                   danger=True)
    except Exception as e:
        print(str(e))
        return render_template("notes.html", str1="Error!! Failure in setting Profile picture!", error=True, danger=True)


@app.route('/backToNote', methods=["POST","GET"])
def backToNote():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")
        print("sesssion = ", email1, pwd1)
        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        return render_template("notes.html")

    except Exception as e:
        print(str(e))
        return render_template("notes.html", str1="Error!! Failure in setting Profile picture!", error=True, danger=True)

################
#############################################
###############################################
################################################



























@app.route('/notes')
def notes():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 != None and pwd1 != None:
            print("going to notes.html : ")
            return render_template("notes.html")
        else:
            return render_template("login.html", str1="Please First Login to use this feature",error=True)

    except KeyError as e:
        print(str(e))
        str1 = "Key Error Occured!!"
        return render_template("login.html", str1=str1, warn1=True)



@app.route('/notes_',methods=["POST","GET"])
def notes_():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion = ",email1,pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,danger1=True)

        print("here")
        filename1=''

        if request.method == "POST":
            title1 = request.form["title1"]
            subject1 = request.form["subject1"]
            content1=request.form["content1"]
            filename1=request.form["fileNotes"]


        else:
            title1  = request.args.get("title1")
            subject1 = request.args.get("subject1")
            content1=request.args.get("content1")
            filename1 = request.args.get("fileNotes")

        print("filename 1 is   ::  ",filename1)
        if filename1=='':
            filename1=None


        if title1==None or subject1==None or content1==None or len(title1)<=0 or len(subject1)<=0 or len(content1)<=0:
            print("zero size true")
            return render_template("notes.html",str1="Warning! Fill all the Form Flied to Add the Notes.",warn1=True,error=True)



        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1,"")
        print(user1)
        userId=DBObj.getId(user1)
        print("User id is : ",userId)


        if filename1!='' and filename1!=None:
            # strFile = filename1.split('.')
            # filename1 = userId + "_" + strFile[0] + "." + strFile[1]
            # print(strFile)
            print("filename is : ", filename1)
            DBObj.addNotes(title1, subject1, content1, userId,filename1)

        else:
            filename1=''
            DBObj.addNotes(title1, subject1, content1, userId,filename1)


        return render_template("notes.html", str1="Notes Added Successfully!!",error=True,success1=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", error="Failed joining")


@app.route('/showNotes')
def showNotes():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)


        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1,pwd1, "")
        userId = DBObj.getId(user1)

        list1 = DBObj.fetchMyNotes(userId)
        print(list1)
        for i in list1:
            print(i)

        pdf1 = False
        pic1 = False
        video1 = False

        listn1=[]
        str2=''
        for list2 in list1:
            list3=[]
            for i in list2:
                list3.append(i)

            if list2[5]!='' and list2[5]!=None:
                str2=list2[5].split('.')
                if str2[1]=='pdf':
                    list3.append('pdf')
                elif str2[1]=='png' or str2[1]=='jpg' or str2[1]=='jpeg':
                    list3.append('pic')
                elif str2[1]=='mp4':
                    list3.append('vd')
            else:
                list3.append('')
            print("str2 == ",str2)
            listn1.append(list3)


        print("list3 is :: ",listn1)

        return render_template("showmynotes.html", data=listn1)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!",error=True,danger=True)


@app.route('/favouriteNotes',methods=["POST","GET"])
def favouriteNotes():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion1 = ",email1,pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,danger1=True)

        if request.method == "POST":
            favId = request.form["notesId"]
        else:
            favId  = request.args.get("notesId")
        print("notes Id = ",favId)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")

        user1 = User("", email1, pwd1,"")
        print(user1)
        userId=DBObj.getId(user1)
        list1 = DBObj.fetchMyNotes(userId)
        print("User id is : ",userId)
        flag=DBObj.checkNoteExist(userId,favId)
        if flag==True:
           flag1= DBObj.checkAlreadyFav(userId,favId)
           if flag1==True:
               return render_template("showmynotes.html",data=list1, str1="Already Included in your favourities", warn1=True, error=True)

           DBObj.addFavNotes(userId,favId)

           return render_template("showmynotes.html",data=list1, str1="Added To Favourities Successfully!!",error=True,success1=True)

        return render_template("showmynotes.html",data=list1, str1="WRONG ID! Notes ID Does Not Exist", warn1=True, error=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Failed joining",error=True,danger1=True)




@app.route('/publicNotes',methods=["POST","GET"])
def publicNotes():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion1 = ",email1,pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,danger1=True)

        if request.method == "POST":
            notesId = request.form["notesId"]
        else:
            notesId = request.args.get("notesId")
        print("notes Id = ",notesId)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")

        user1 = User("", email1, pwd1,"")
        print(user1)
        userId=DBObj.getId(user1)
        list1 = DBObj.fetchMyNotes(userId)
        print("User id is : ",userId)

        flag=DBObj.checkNoteExist(userId,notesId)
        if flag==True:
           flag1= DBObj.checkAlreadyPublic(userId,notesId)
           if flag1==True:
               return render_template("showmynotes.html",data=list1, str1="Your notes are already Public.", warn1=True, error=True)

           DBObj.publicPrivateNotes(userId,notesId)

           return render_template("showmynotes.html",data=list1, str1="Your notes are public now Successfully!!",error=True,success1=True)

        return render_template("showmynotes.html",data=list1, str1="WRONG ID! Notes ID Does Not Exist", warn1=True, error=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Failed joining",error=True,danger1=True)


@app.route('/privateNotes',methods=["POST","GET"])
def privateNotes():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion1 = ",email1,pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,danger1=True)

        if request.method == "POST":
            notesId = request.form["notesId"]
        else:
            notesId = request.args.get("notesId")
        print("notes Id = ",notesId)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")

        user1 = User("", email1, pwd1,"")
        print(user1)
        userId=DBObj.getId(user1)
        list1 = DBObj.fetchMyNotes(userId)
        print("User id is : ",userId)

        flag=DBObj.checkNoteExist(userId,notesId)
        if flag==True:
           flag1= DBObj.checkAlreadyPublic(userId,notesId)
           if flag1==False:
               return render_template("showmynotes.html",data=list1, str1="Your notes are already Private.", warn1=True, error=True)

           DBObj.publicPrivateNotes(userId,notesId,privateNotes=True)

           return render_template("showmynotes.html",data=list1, str1="Your notes are private now Successfully!!",error=True,success1=True)

        return render_template("showmynotes.html",data=list1, str1="WRONG ID! Notes ID Does Not Exist", warn1=True, error=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Failed joining",error=True,danger1=True)


@app.route('/showFavNotes')
def showFavNotes():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)


        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1,pwd1, "")
        userId = DBObj.getId(user1)

        list1 = DBObj.fetchMyNotes(userId,fav=True)

        pdf1 = False
        pic1 = False
        video1 = False

        listn1 = []
        str2 = ''
        for list2 in list1:
            list3 = []
            for i in list2:
                list3.append(i)

            if list2[5] != '' and list2[5] != None:
                str2 = list2[5].split('.')
                if str2[1] == 'pdf':
                    list3.append('pdf')
                elif str2[1] == 'png' or str2[1] == 'jpg' or str2[1] == 'jpeg':
                    list3.append('pic')
                elif str2[1] == 'mp4':
                    list3.append('vd')
            else:
                list3.append('')
            print("str2 == ", str2)
            listn1.append(list3)

        print("list3 is :: ", listn1)

        return render_template("showmynotes.html", data=listn1,fav1=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!",error=True,danger=True)



@app.route('/showAllNotes')
def showAllNotes():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)


        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1,pwd1, "")
        userId = DBObj.getId(user1)

        list1 = DBObj.fetchMyNotes(userId,fav=True,allNotes=True)

        pdf1 = False
        pic1 = False
        video1 = False

        listn1 = []
        str2 = ''
        for list2 in list1:
            list3 = []
            for i in list2:
                list3.append(i)

            if list2[5] != '' and list2[5] != None:
                str2 = list2[5].split('.')
                if str2[1] == 'pdf':
                    list3.append('pdf')
                elif str2[1] == 'png' or str2[1] == 'jpg' or str2[1] == 'jpeg':
                    list3.append('pic')
                elif str2[1] == 'mp4':
                    list3.append('vd')
            else:
                list3.append('')
            print("str2 == ", str2)
            listn1.append(list3)

        print("list3 is :: ", listn1)

        return render_template("showmynotes.html", data=listn1,allNotes1=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!",error=True,danger=True)



@app.route('/calculator')
def calculator():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        return render_template("eight.html")

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)





@app.route('/home')
def home():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        return render_template("home.html")

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)



@app.route('/showTimer')
def showTimer():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        return render_template("timer.html")

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)


@app.route("/logout")
def logout():
    try:

        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("session = em pwd ",email1,pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", error=True, str1="Please First Login to use this feature")

        session.clear()
        return render_template("login.html")
    except KeyError as e:
        print(str(e))
        str1="Key Error Occured!!"
        return render_template("home.html",str1=str1,warn1=True)


@app.route('/addSubject')
def addSubject():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 != None and pwd1 != None:
            print("going to addSubject.html : ")
            return render_template("addSubject.html")
        else:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,danger1=True)

    except KeyError as e:
        print(str(e))
        str1 = "Key Error Occured!!"
        return render_template("login.html", str1=str1, warn1=True)


@app.route('/addSubject_',methods=["POST","GET"])
def addSubject_():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion sub = ",email1,pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,danger1=True)

        if request.method == "POST":
            subject1 = request.form["subject1"]
        else:
            subject1 = request.args.get("subject1")

        if subject1==None or len(subject1)<=0:
            print("zero size true")
            return render_template("addSubject.html",str1="Warning! Fill all the Form Flied to Add the Notes.",warn1=True,error=True)


        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1,"")
        print(user1)
        userId=DBObj.getId(user1)
        print("User id is : ",userId)

        flag1=DBObj.checkSubExist(userId,subject1)
        if flag1==True:
            return render_template("addSubject.html", str1="Warning!Subject Already Exist.",
                                   warn1=True, error=True)

        DBObj.addSubject(userId,subject1)
        print("subject added successfully")
        return render_template("addSubject.html", str1="Subject Added Successfully!!",success1=True,error=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", error="Failed joining")



@app.route('/showSubject')
def showSubject():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)


        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1,pwd1, "")
        userId = DBObj.getId(user1)

        list1 = DBObj.fetchMySubjects(userId)
        return render_template("showSubject.html", data1=list1)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!",error=True,danger=True)


@app.route("/deleteSubject")
def deleteSubject():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 != None and pwd1 != None:
            print("going to deleteSubject.html-- : ")
            return render_template("deleteSubject.html")
        else:
            return render_template("login.html", str1="Please First Login to use this feature", error=True)

    except KeyError as e:
        print(str(e))
        str1 = "Key Error Occured!!"
        return render_template("login.html", str1=str1, warn1=True)






@app.route('/deleteSubject_',methods=["POST","GET"])
def deleteSubject_():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion sub = ",email1,pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,danger1=True)

        if request.method == "POST":
            subject1 = request.form["subject1"]
        else:
            subject1 = request.args.get("subject1")

        if subject1==None or len(subject1)<=0:
            print("zero size true")
            return render_template("deleteSubject.html",str1="Warning! Fill all the Form Field to Delete.",warn1=True,error=True)



        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1,"")
        print(user1)
        userId=DBObj.getId(user1)
        print("User id is : ",userId)

        flag1=DBObj.checkSubExist(userId,subject1)
        if flag1==True:
            DBObj.deleteSubject(userId, subject1)
            return render_template("deleteSubject.html", str1="SUBJECT DELETED SUCCESSFULLY!!!",
                                   success1=True, error=True)
        return render_template("deleteSubject.html", str1="ALERT!!!  SUBJECT NOT EXIST!\nENTER CORRECT SUBJECT NAME.",
                           danger1=True, error=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", error="Failed joining")


@app.route("/reportQuestion")
def reportQuestion():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 != None and pwd1 != None:
            print("going to reportQuestion.html : ")
            return render_template("reportQuestion.html")
        else:
            return render_template("login.html", str1="Please First Login to use this feature",error=True,danger=True)

    except KeyError as e:
        print(str(e))
        str1 = "Key Error Occured!!"
        return render_template("login.html", str1=str1, warn1=True)

@app.route("/reportQuestion_",methods=["POST","GET"])
def reportQuestion_():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion = ",email1,pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,danger1=True)

        if request.method == "POST":
            title1 = request.form["title1"]
            content1=request.form["content1"]
        else:
            title1  = request.args.get("title1")
            content1=request.args.get("content1")

        if title1==None or content1==None or len(title1)<=0 or len(content1)<=0:
            print("zero size true")
            return render_template("reportQuestion.html",str1="Warning! Fill all the Form Flied to Add the Notes.",warn1=True,error=True)



        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1,"")
        print(user1)
        userId=DBObj.getId(user1)
        print("User id is1 : ",userId)



        DBObj.addQuestion(title1,content1,userId)
        return render_template("reportQuestion.html", str1="Question reported Successfully!!",error=True,success1=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", error="Failed joining")


@app.route('/showQuestions')
def showQuestions():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        redirect(url_for('showQuestions'))


        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")


        list1 = DBObj.fetchQuestions()

        listcm=[]
        for qs in list1:
            c1=[]
            for i in qs:
                c1.append(i)


            print("qId = ",qs[0])
            coms=DBObj.fetchComments(qs[0])
            print("com1 = ",coms)
            c1.append(coms)
            listcm.append(c1)


        print("List with comment is : ",len(listcm),listcm)

        print("question list --> ",list1)

        return render_template("showQuestions.html", data=listcm)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!",error=True,danger=True)


@app.route("/addComment",methods=["POST","GET"])
def addComment():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion = ", email1, pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        if request.method == "POST":
            qId = request.form["qId"]
        else:
            qId = request.args.get("qId")
            print("QUESTION ID == ",qId)

        return render_template("addComment.html",qId=qId)

    except Exception as e:
        print(str(e))
        return render_template("login.html", error="Failed joining")



@app.route("/addComment_",methods=["POST","GET"])
def addComment_():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion = ", email1, pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        if request.method == "POST":
            qId = request.form["qId"]
            content=request.form["content1"]
        else:
            qId = request.args.get("qId")
            content=request.args.get("content1")

        print("QUESTION ID == ",qId)
        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1,"")
        userId = DBObj.getId(user1)
        print("User id is1 : ", userId,str(content))

        DBObj.addComment(str(qId),str(content),userId)

        list1 = DBObj.fetchQuestions()

        listcm=[]
        for qs in list1:
            c1=[]
            for i in qs:
                c1.append(i)

            print("qId = ",qs[0])
            coms=DBObj.fetchComments(qs[0])
            print("com1 = ",coms)
            c1.append(coms)
            listcm.append(c1)


        print("List with comment is : ",len(listcm),listcm)

        print("question list --> ",list1)


        redirect(url_for('showQuestions'))
        return render_template("showQuestions.html",data=listcm,str1="YOUR COMMENT ADDED SUCCESSFULLY!!!!",error=True,success1=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", error="Failed joining")






@app.route('/showComments', methods=["POST", "GET"])
def showComments():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion = ", email1, pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)
        if request.method == "POST":
            qId = request.form["qId"]
        else:
            qId = request.args.get("qId")
        print("QUESTION ID == ", qId)

        print("QUESTION ID == ", qId)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        list1 = DBObj.fetchComments(qId)
        return render_template("showComments.html", data=list1)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)


@app.route('/deleteQuestion', methods=["POST", "GET"])
def deleteQuestion():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion = ", email1, pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        if request.method == "POST":
            qId = request.form["qId"]
            uId = request.form['userId']
        else:
            qId = request.args.get("qId")
            uId = request.args.get("userId")

        print("QUESTION ID == ", qId)


        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1, "")
        userId = DBObj.getId(user1)
        list1 = DBObj.fetchQuestions()

        if userId != uId:
            str1 = "Warning!! You are not allowed to delete this Question"
            "you can delete only your uploaded Question!"
            return render_template("showQuestions.html", data=list1,str1=str1, error=True, warn1=True)


        DBObj.deleteQuestion(qId)
        str1 = "Your Question deleted Successfully!!"
        return render_template("showQuestions.html",data=list1, str1=str1, error=True, success1=True)
    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)


##################


@app.route("/profile")
def defaultProfile():
    email=session.get("uemail")
    pwd=session.get("upwd")

    if email==None and pwd==None:
        return render_template("error.html")
    DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
    imgName=DBObj.getUserProfilePic(email)
    list=DBObj.getUserAllData(email)
    print("list extracted -- \n")
    print(list)

    uFirstName=list[0][8]
    uLastName=list[0][9]
    udob=list[0][10]
    # uBio=[0][11]
    uBio=DBObj.getUserBio(email)
    uPhoneNo=DBObj.getUserPhoneNo(email)
    uDegree=DBObj.getUserDegree(email)
    uUniversity=DBObj.getUserUniversity(email)
    uCountry=DBObj.getUserCountry(email)
    gender=DBObj.getGender(email)

    print("img is :: ",imgName)

    if imgName == None or imgName == "":
        imgName = "usericon.png"

    if uFirstName==None:
        uFirstName=""

    if uLastName==None:
        uLastName=""

    if uBio==None:
        uBio=""

    if udob==None:
        udob=""

    if uPhoneNo==None:
        uPhoneNo=""

    if uDegree==None:
        uDegree==""

    if uUniversity==None:
        uUniversity=""

    if uCountry==None:
        uCountry=""


    return render_template("profile.html",imageName=imgName ,userEmail=email, userPassword=pwd, userFirstName= uFirstName,
                           userLastName=uLastName,userdob=udob, userBio=uBio,userPhoneno=uPhoneNo,
                           userDegree=uDegree, userUniversity=uUniversity, userCountry=uCountry,gender=gender)

#profile
@app.route("/profileManage",methods=["GET","POST"])
def profileManage():
    print("profile function manage called")
    email = session.get("uemail")
    pwd = session.get("upwd")
    print(email,"   ",pwd)

    DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
    user1 = User("", email, pwd, "")

    if request.method=="POST":
        fname=request.form["firstName"]
        lname=request.form["lastName"]
        email=request.form["email"]
        password=request.form["password"]
        bio = request.form["bio"]
        dob = request.form["dob"]
        phoneNo = request.form["phoneNo"]
        country = request.form["country"]
        uniName = request.form["uniName"]
        degree = request.form["degree"]
        if (request.form["check"] == "male"):
            gender = "male"
        elif (request.form["check"] == "female"):
            gender = "female"
        else:
            gender = "other"
        print("gender is : ",gender)
    else:
        fname = request.args.get("firstName")
        lname = request.args.get("lastName")
        email = request.args.get("email")
        password = request.args.get("password")
        bio = request.args.get("bio")
        dob = request.args.get("dob")
        phoneNo = request.args.get("phoneNo")
        country = request.args.get("country")
        uniName =request.args.get("uniName")
        degree = request.args.get("degree")
        if (request.args.get("check") == "male"):
            gender = "male"
        elif (request.args.get("check") == "female"):
            gender = "female"
        else:
            gender = "other"

    user1 = User("", email, pwd, "")

    userId = DBObj.getId(user1)

    imageName=DBObj.getUserProfilePic(email)

    piclink = imageName
    userAcc=Profile(fname,lname,email,password,bio,dob,phoneNo,country,uniName,degree,gender,piclink,userId)

    DBObj.addUserProfile(userAcc)

    return render_template("home.html",str1="Profile Updated Successfully",succcess1=True,error=True )



def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route("/editprofilepic", methods=['GET','POST'])
def index():
    try:
        print("in index")
        files = os.listdir("static")
        return render_template('profileindex.html', files=files)
    except Exception as e:
        print("Exception in Edit Profile Picture", str(e))
        return "Hello world"

@app.route("/editprofilepic2", methods=['GET','POST'])
def upload_files():
    print("in upload_files")
    uploaded_file = request.files['file']
    print("1")
    filename = secure_filename(uploaded_file.filename)
    print(filename)

    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")
        print("sesssion = ", email1, pwd1)
        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)
        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        list1 = DBObj.setUserProfilePic(email1,filename)
        if list1==True:
            print("2")
            if filename != '':
                print("3")
                file_ext = os.path.splitext(filename)[1]
                print("4")
                if file_ext not in  ['.jpg', '.png', '.jpeg'] or file_ext != validate_image(uploaded_file.stream):
                    print("5")
                    abort(400)
                print("6")
                uploaded_file.save(os.path.join("static", filename))
                print("7")
            return redirect(url_for('index'))
        else:
            return render_template("Profile.html", str1="Error!! Failure in setting Profile picture!", error=True,
                                   danger=True)
    except Exception as e:
        print(str(e))
        return render_template("Profile.html", str1="Error!! Failure in setting Profile picture!", error=True, danger=True)

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory("static", filename)

@app.route('/backToProfile', methods=["POST","GET"])
def backToProfile():
    # imgname="nature.jpg"
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")
        print("sesssion = ", email1, pwd1)
        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")

        imgName = DBObj.getUserProfilePic(email1)
        list = DBObj.getUserAllData(email1)
        print("list extracted -- \n")
        print(list)

        uFirstName = list[0][8]
        uLastName = list[0][9]
        udob = list[0][10]
        # uBio=[0][11]
        uBio = DBObj.getUserBio(email1)
        uPhoneNo = DBObj.getUserPhoneNo(email1)
        uDegree = DBObj.getUserDegree(email1)
        uUniversity = DBObj.getUserUniversity(email1)
        uCountry = DBObj.getUserCountry(email1)
        gender = DBObj.getGender(email1)
        print("pict === ",imgName)

        if imgName==None or imgName=="":
            imgName="usericon.png"

        return render_template("profile.html", imageName=imgName, userEmail=email1, userPassword=pwd1,
                               userFirstName=uFirstName,
                               userLastName=uLastName, userdob=udob, userBio=uBio, userPhoneno=uPhoneNo,
                               userDegree=uDegree, userUniversity=uUniversity, userCountry=uCountry, gender=gender)

    except Exception as e:
        print(str(e))
        return render_template("Profile.html", str1="Error!! Failure in setting Profile picture!", error=True, danger=True)

################


@app.route('/viewUsers',methods=["GET","POST"])
def viewUsers():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)


        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1,pwd1, "")
        userId = DBObj.getId(user1)

        list1 = DBObj.fetchUsers(userId)
        print(list1)
        list2=[]

        for user1 in list1:
            imgName=DBObj.getUserProfilePic(user1[3])
            if imgName==None or imgName=="":
                imgName="usericon.png"
                list2.append(imgName)
           # user1[17]=imgName

        return render_template("viewUsers.html", data=list1,list2=list2)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing Users!",error=True,danger=True)



@app.route("/addConnection",methods=["POST","GET"])
def addConnection():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")


        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1, "")
        userId = DBObj.getId(user1)
        list1 = DBObj.fetchUsers(userId)

        if request.method == "POST":
            userId1 = request.form["userId1"]
        else:
            userId1 = request.args.get("userId1")

        print("User1 == ", userId1)

        conSt=DBObj.checkConnection(userId,userId1)
        if(conSt==True):
            return render_template("viewUsers.html",data=list1, str1="You are Already in Connection with User!!!",error=True,warn1=True)


        DBObj.addNotification(userId,userId1)
        return render_template("viewUsers.html",data=list1, str1="Connection Request Send Successfully To User!", error=True, Succes=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", error="Failed joining")




@app.route('/showNotifications')
def showNotifications():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)


        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1,pwd1, "")
        userId = DBObj.getId(user1)

        list1 = DBObj.fetchNotifications(userId)
        # userNames=[]
        # for n in list1:
        #     userNames.append(DBObj.getUserName(n[6]))
        print("list of notf are :: ",list1)

        userImg="../static/usericon.png"
        listn1=[]
        for list2 in list1:
            list3=[]
            for i in list2:
                list3.append(i)
            userImg=DBObj.getUserImage(list2[4])
            print("uimg is  ",userImg)
            list3.append(userImg)
            listn1.append(list3)
        print("final notf list is :: ",listn1)


        return render_template("showNotifications.html", data=listn1,userImg=userImg)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing Users!",error=True,danger=True)



@app.route("/acceptNotification",methods=["POST","GET"])
def acceptNotification():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")


        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1, "")
        userId = DBObj.getId(user1)

        if request.method == "POST":
            userId2 = request.form["userId2"]
        else:
            userId2 = request.args.get("userId2")

        print("User2 == ", userId2,"  ",userId)

        DBObj.connectUser(userId,userId2)

        DBObj.delNotification(userId,userId2)
        DBObj.delNotification(userId2, userId)
        list1 = DBObj.fetchNotifications(userId)

        return render_template("showNotifications.html",data=list1, str1="Connected Successfully To User!", error=True, Succes=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", error="Failed joining")



@app.route("/delNotification",methods=["POST","GET"])
def delNotification():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")


        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1, "")
        userId = DBObj.getId(user1)

        if request.method == "POST":
            userId2 = request.form["userId2"]
        else:
            userId2 = request.args.get("userId2")

        print("User2 == ", userId2,"  ",userId)

        DBObj.delNotification(userId,userId2)

        list1 = DBObj.fetchNotifications(userId)

        return render_template("showNotifications.html",data=list1, str1="Connection Decline!", error=True, Succes=True)

    except Exception as e:
        print(str(e))
        return render_template("login.html", error="Failed joining")


@app.route("/showConnections")
def showConnections():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1, "")
        userId = DBObj.getId(user1)

        list1 = DBObj.getConnections(userId)
        print("connecetions -->> ",list1)

        for user1 in list1:
            imgName=DBObj.getUserProfilePic(user1[3])
            if imgName==None or imgName=="":
                imgName="usericon.png"

        return render_template("showConnections.html", data=list1)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)

@app.route('/chatting')
def chatting():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        return render_template("index.html")

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)



@app.route('/showNotesSubjects', methods=["POST", "GET"])
def showNotesSubjects():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion = ", email1, pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        list1 = DBObj.getNotesCategories()
        print("categories= ",list1)
        return render_template("shownotescategories.html", data=list1)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)


@app.route('/showSpecificCategory', methods=["POST", "GET"])
def showSpecificCategory():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        print("sesssion = ", email1, pwd1)

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)
        if request.method == "POST":
            subName = request.form["subName"]
        else:
            subName = request.args.get("subName")
        print("QUESTION ID == ",subName)

        print("QUESTION ID == ", subName)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1, "")
        userId = DBObj.getId(user1)

        list1 = DBObj.getSpecificNotes(subName,userId)

        pdf1 = False
        pic1 = False
        video1 = False

        print("In notes categories")
        listn1 = []
        str2 = ''
        for list2 in list1:
            list3 = []
            for i in list2:
                list3.append(i)

            if list2[5] != '' and list2[5] != None:
                str2 = list2[5].split('.')
                if str2[1] == 'pdf':
                    list3.append('pdf')
                elif str2[1] == 'png' or str2[1] == 'jpg' or str2[1] == 'jpeg':
                    list3.append('pic')
                elif str2[1] == 'mp4':
                    list3.append('vd')
            else:
                list3.append('')
            print("str2 == ", str2)
            listn1.append(list3)

        print("list3 is :: ", listn1)

        return render_template("showmynotes.html",data=listn1,specificNotes=True,subName=subName)

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)



@app.route('/timerTimming',methods=["GET","POST"])
def timerTimming():
    if request.method=="POST":
        min = request.form["minTime"]
        sec = request.form["secTime"]
        minb = request.form["minTimeBreak"]
        secb = request.form["secTimeBreak"]

    else:
        min = request.args.get("minTime")
        sec = request.args.get("secTime")
        minb = request.args.get("minTimeBreak")
        secb = request.args.get("secTimeBreak")

    return render_template("PomodoroTimer.html", minTime=min, secTime=sec, minTimeBreak=minb, secTimeBreak=secb)



@app.route('/todolist')
def todoList():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1, "")
        userId = DBObj.getId(user1)
        userName1=DBObj.getUserName(userId)
        print(userName1[0][0])

        return render_template("todoList.html",userId=userId,userName=str(userName1[0][0]))

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)



@app.route('/showTodoList')
def showTodoList():
    try:
        email1 = session.get("uemail")
        pwd1 = session.get("upwd")

        if email1 == None and pwd1 == None:
            return render_template("login.html", str1="Please First Login to use this feature", error=True,
                                   danger1=True)

        DBObj = DataBaseHandler("localhost", "root", '', "studyplanner")
        user1 = User("", email1, pwd1, "")
        userId = DBObj.getId(user1)
        userName1=DBObj.getUserName(userId)
        print(userName1[0][0])

        return render_template("showTD.html",userId=userId,userName=str(userName1[0][0]))

    except Exception as e:
        print(str(e))
        return render_template("login.html", str1="Error!! Failure in showing notes!", error=True, danger=True)


if __name__ == '__main__':
    app.run(debug=True)

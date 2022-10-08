
from Classes import User,TodoList
import pymysql

class DataBaseHandler:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.con = None

        try:
            self.con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.database)
        except Exception as e:
            print("There is error in connection", str(e))

    def __del__(self):
        if self.con != None:
            self.con.close()

    def checkUserExist(self, user1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from useraccount where user_email=%s and user_password=%s;"

                args = (user1.email,user1.password)
                cur.execute(query1, args)
                rows = cur.fetchall()
                print( "rows are : ",rows)
                cur.close()
                if (len(rows) == 0):
                    return False
                else:
                    return True

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def addUser(self, user2):
        try:
            if self.con != None:
                cur = self.con.cursor()
                if user2.acc_type == "TEACHER":
                    acc=1
                else:
                    acc=2
                query1 = "Insert into useraccount(user_name,user_email,user_password,user_acc_type) values(%s,%s,%s,%s);"

                args = (user2.name, user2.email, user2.password,acc)
                cur.execute(query1, args)
                self.con.commit()
                query2 = "update useraccount set user_id=concat(user_str,user_no);"

                cur.execute(query2)
                self.con.commit()

                query3 = "select user_id from useraccount where user_email=%s;"
                args = (user2.email)
                cur.execute(query3, args)
                self.con.commit()
                rows=cur.fetchall()

                print("add rows= ",query3)
                if len(rows)<=0:
                    return False
                return True

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def getId(self, user):
        try:
            if self.con != None:
                cur = self.con.cursor()
            query1 = "select user_id from UserAccount where user_email=%s and user_password=%s"
            args = (user.email,user.password)
            cur.execute(query1, args)
            id = cur.fetchall()
            print("user id is = ",id)
            return id[0][0]
        except Exception as e:
            print("exception in id ",str(e))
        finally:
            if cur != None:
                cur.close()

    def addNotes(self, title1,subject1,content1,userId,filename1=''):
        try:
            if self.con != None:
                cur = self.con.cursor()
                subject1=subject1.upper();
                print("sub--> ",subject1,"  ",title1,"  ",content1,"  ",userId,"  ",filename1)
                query1 = "insert into Notes (notes_title,notes_subject,notes_content,user_id,file_uploaded)" \
                         " values(%s,%s,%s,%s,%s);"
                args = (title1,subject1,content1,userId,filename1)
                cur.execute(query1, args)
                self.con.commit()

                query2 = "update Notes set notes_id=concat(notes_str,notes_no);"
                cur.execute(query2)
                self.con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def fetchMyNotes(self,userId,fav=False,allNotes=False):
        try:
            if self.con != None:
                cur = self.con.cursor()
                if allNotes==False:
                    if fav==False:
                        query1 = "select notes_title,notes_subject,notes_content,nt_date_created,notes_id, file_uploaded from notes" \
                                 " where user_id=%s;"
                    elif fav==True:
                        query1 = "select notes_title,notes_subject,notes_content,nt_date_created,notes_id,file_uploaded" \
                                 " from notes" \
                                 " where user_id=%s and notes_favSt=1;"
                    args = (userId)
                    cur.execute(query1, args)

                else:
                    query1 = "select notes_title,notes_subject,notes_content,nt_date_created,notes_id,file_uploaded from notes" \
                             " where  notes_publicSt=1;"

                    cur.execute(query1)

                notesList = cur.fetchall()
                print(notesList)
                return notesList
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def addFavNotes(self,userId,favId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                st=1
                query1 = "update notes set notes_favSt=%s where user_id=%s and notes_id=%s;"
                args = (st,userId,favId)
                cur.execute(query1, args)
                self.con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def checkNoteExist(self, userId, favId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from notes where user_id=%s and notes_id=%s;"

                args = (userId, favId)
                cur.execute(query1, args)
                rows = cur.fetchall()

                print("rows are : ", rows)
                cur.close()
                if (len(rows) == 0):
                    return False
                else:
                    return True

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def checkAlreadyFav(self, userId, favId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from notes where user_id=%s and notes_id=%s and notes_favSt=1;"

                args = (userId, favId)
                cur.execute(query1, args)
                rows = cur.fetchall()

                print("rows are : ", rows)
                cur.close()
                if (len(rows) == 0):
                    return False
                else:
                    return True

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def checkSubExist(self, userId, subName):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from subject where user_id=%s and sub_name=%s;"

                args = (userId, subName)
                cur.execute(query1, args)
                rows = cur.fetchall()

                print("rows are : ", rows)
                cur.close()
                if (len(rows) == 0):
                    return False
                else:
                    return True

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()



    def addSubject(self,userId,subName):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "insert into subject (sub_name,user_id) values(%s,%s);"
                args = (subName,userId)
                cur.execute(query1, args)
                self.con.commit()

                query2 = "update subject set sub_id=concat(sub_str,sub_no);"
                cur.execute(query2)
                self.con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def fetchMySubjects(self, userId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select sub_id,sub_name,sub_date from subject where user_id=%s;"

                args = (userId)
                cur.execute(query1, args)
                subList = cur.fetchall()
                print(subList)
                return subList
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def deleteSubject(self,userId,subName):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "delete from subject where user_id=%s and sub_name=%s;"
                args = (userId,subName)
                cur.execute(query1, args)
                self.con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()



    def addQuestion(self, title1, content1, userId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "insert into Questions (q_name,q_content,user_id) values(%s,%s,%s);"
                args = (title1, content1, userId)
                cur.execute(query1, args)
                self.con.commit()

                query2 = "update Questions set q_id=concat(q_str,q_no);"
                cur.execute(query2)
                self.con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def fetchQuestions(self):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select q_id,q_name,q_content,q_date,user_id from questions"
                cur.execute(query1)
                questList = cur.fetchall()
                print(questList)
                return questList
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def addComment(self,qId,content,userId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "insert into comments (q_id,com_content,user_id ) values(%s,%s,%s);"
                args = (qId,content,userId)
                cur.execute(query1, args)
                self.con.commit()

                query2 = "update comments set com_id=concat(com_str,com_no);"
                cur.execute(query2)
                self.con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def fetchComments(self,qId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select com_id,com_content,com_time,user_id from comments where q_id=%s"
                args=(qId)
                cur.execute(query1,args)
                questList = cur.fetchall()
                print(questList)
                return questList
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def deleteQuestion(self,qId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "delete from comments where q_id=%s;"
                args = (qId)
                cur.execute(query1, args)
                self.con.commit()

                query2 = "delete from Questions where q_id=%s;"
                args = (qId)
                cur.execute(query2, args)
                self.con.commit()
                print("deleted successfully")

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def addUserProfile(self, userp):
        # Write your code here
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "UPDATE userAccount SET user_first_name=%s, user_last_name=%s,user_dob=%s," \
                        "user_bio=%s,user_gender=%s,user_institution=%s," \
                        "user_country=%s,user_field=%s,user_phone_number=%s, User_img_path=%s WHERE user_id=%s"
                args = (userp.fname, userp.lname, userp.dob, userp.bio, userp.gender, userp.uniName,
                        userp.country, userp.degree, userp.phoneNo, userp.piclink, userp.userId)

                cur.execute(query, args)
                self.con.commit()
                return True
            else:
                print("---AddingProfileFailed---")
                return False
        except Exception as e:
            print("Exception in inserting profile", str(e))
            print("---AddingProfileFailed---")
            return False
        finally:
            if cur != None:
                cur.close()

    def setUserProfilePic(self, email, picname):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "UPDATE userAccount SET User_img_path=%s WHERE user_email=%s;"
                args = (picname, email)
                cur.execute(query, args)
                self.con.commit()
                print("insetuserprofilepic")
                return True
            else:
                print("---AddingProfilePictureFailed---")
                return False
        except Exception as e:
            print("Exception in inserting profile Picture", str(e))
            print("---AddingProfilePictureFailed---")
            return False
        finally:
            if cur != None:
                cur.close()

    def getUserProfilePic(self, email1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT USER_IMG_PATH from useraccount where user_email=%s;"
                args = (email1)
                cur.execute(query, args)
                x = cur.fetchall()
                print(x)
                self.con.commit()
                print("getuserprofilepic")
                print("img is --> ",x)

                if x==None or x=="" or len(x)==0:
                    return "usericon.png"
                return x[0][0]

        except Exception as e:
            print("Exception in inserting profile Picture", str(e))
            return False
        finally:
            if cur != None:
                cur.close()

    def getUserFirstName(self, email1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT User_first_name from useraccount where user_email=%s;"
                args = (email1)
                cur.execute(query, args)
                x = cur.fetchall()
                self.con.commit()
                return x[0][0]
            else:
                print("---GettingFirstNameFailed---")
                return False
        except Exception as e:
            print("Exception in inserting profile Picture", str(e))
            print("---GettingFirstNameFailed---")
            return False
        finally:
            if cur != None:
                cur.close()

    def getGender(self,email1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT user_gender from useraccount where user_email=%s;"
                args = (email1)
                cur.execute(query, args)
                x = cur.fetchall()
                self.con.commit()
                print(x[0][0])
                return x[0][0]
        except Exception as e:
            print("Exception in getting gender", str(e))
            return False
        finally:
            if cur != None:
                cur.close()


    def getUserBio(self, email1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT user_bio from useraccount where user_email=%s;"
                args = (email1)
                cur.execute(query, args)
                x = cur.fetchall()
                print(x)
                self.con.commit()
                return x[0][0]
            else:
                print("---GettingUserDataForProfileFailed---")
                return False
        except Exception as e:
            print("Exception in geeting all data for profile", str(e))
            print("---GettingUserDataForProfileFailed---")
            return False
        finally:
            if cur != None:
                cur.close()

    def getUserPhoneNo(self, email1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT user_phone_number from useraccount where user_email=%s;"
                args = (email1)
                cur.execute(query, args)
                x = cur.fetchall()
                print(x)
                self.con.commit()
                return x[0][0]
            else:
                print("---GettingUserPhone numberFailed---")
                return False
        except Exception as e:
            print("Exception in geeting all data for profile", str(e))
            print("---GettingUserDataForProfileFailed---")
            return False
        finally:
            if cur != None:
                cur.close()

    def getUserDegree(self, email1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT user_field from useraccount where user_email=%s;"
                args = (email1)
                cur.execute(query, args)
                x = cur.fetchall()
                print(x)
                self.con.commit()
                return x[0][0]
            else:
                print("---GettingUserfieldFailed---")
                return False
        except Exception as e:
            print("Exception in getting field data for profile", str(e))
            print("---GettingUserDataForProfileFailed---")
            return False
        finally:
            if cur != None:
                cur.close()

    def getUserUniversity(self, email1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT user_institution from useraccount where user_email=%s;"
                args = (email1)
                cur.execute(query, args)
                x = cur.fetchall()
                print(x)
                self.con.commit()
                return x[0][0]
            else:
                print("---GettingUserPhone numberFailed---")
                return False
        except Exception as e:
            print("Exception in geeting all data for profile", str(e))
            print("---GettingUserDataForProfileFailed---")
            return False
        finally:
            if cur != None:
                cur.close()

    def getUserCountry(self, email1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT user_country from useraccount where user_email=%s;"
                args = (email1)
                cur.execute(query, args)
                x = cur.fetchall()
                print(x)
                self.con.commit()
                return x[0][0]
            else:
                print("---GettingUserCountryFailed---")
                return False
        except Exception as e:
            print("Exception in geeting country data for profile", str(e))
            print("---GettingUserDataForProfileFailed---")
            return False
        finally:
            if cur != None:
                cur.close()

    def getUserAllData(self, email1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT * from useraccount where user_email=%s;"
                args = (email1)
                cur.execute(query, args)
                x = cur.fetchall()
                print("getuserAlldata --> \n")
                print(x)
                self.con.commit()
                return x
            else:
                print("---GettingUserDataForProfileFailed---")
                return False
        except Exception as e:
            print("Exception in geeting all data for profile", str(e))
            print("---GettingUserDataForProfileFailed---")
            return False
        finally:
            if cur != None:
                cur.close()


    def checkAlreadyPublic(self, userId, notesId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from notes where user_id=%s and notes_id=%s and notes_publicSt=1;"
                args = (userId, notesId)
                cur.execute(query1, args)
                rows = cur.fetchall()

                print("rows are : ", rows)
                cur.close()
                if (len(rows) == 0):
                    return False
                else:
                    return True

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()



    def  publicPrivateNotes(self,userId,notesId,privateNotes=False):
        try:
            if self.con != None:
                cur = self.con.cursor()

                if privateNotes==False:
                    st = 1
                    query1 = "update notes set notes_publicSt=%s where user_id=%s and notes_id=%s;"
                else:
                    st = 0
                    query1 = "update notes set notes_publicSt=%s where user_id=%s and notes_id=%s;"

                args = (st,userId,notesId)
                cur.execute(query1, args)
                self.con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()




    def fetchUsers(self,id):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from UserAccount where user_id != %s"
                args = (id)
                cur.execute(query1,args)
                users = cur.fetchall()
                print(users)
                return users
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def checkConnection(self,user1,user2):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from Connections where user_id1 = %s and user_id2=%s and conn_st=1;"
                args = (user1,user2)
                cur.execute(query1, args)
                users = cur.fetchall()

                query2 = "select * from Connections where user_id1 = %s and user_id2=%s and conn_st=1;"
                args = (user2, user1)
                cur.execute(query2, args)
                users1= cur.fetchall()


                print(users)
                if (len(users) == 0 and len(users1)==0):
                    return False
                else:
                    return True
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def addNotification(self,user1,user2):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "insert into Notifications (user_id1,user_id2,notf_st) values(%s,%s,1);"
                args = (user1, user2)
                cur.execute(query1, args)
                self.con.commit()

                query2 = "update Notifications set notf_id=concat(notf_str,notf_no);"
                cur.execute(query2)
                self.con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def fetchNotifications(self,user1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from Notifications where user_id2 = %s"
                args = (user1)
                cur.execute(query1, args)
                users = cur.fetchall()
                print(users)

                tupUsers = ()
                for k in reversed(users):
                    tupUsers = tupUsers + (k,)

                list11=[]
                for u1 in tupUsers:
                    query1 = "select * from useraccount where user_id = %s"
                    args = (u1[4])
                    cur.execute(query1, args)
                    us1 = cur.fetchall()

                    list11.append(us1[0])
                print("list nitify by -- > ",list11)

                print(tupUsers)

                print()
                myList=[]
                myList.append(tupUsers,)
                return tupUsers
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def getUserName(self,userId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select user_name from UserAccount where user_id = %s"
                args = (userId)
                cur.execute(query1, args)
                users = cur.fetchall()
                print(users)

                return users
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def delNotification(self,userId1,userId2):
        try:
            if self.con != None:
                print(userId1,"  ",userId2)
                cur = self.con.cursor()
                query1 = "delete from Notifications where user_id2=%s and user_id1=%s;"
                args = (userId1,userId2)
                cur.execute(query1, args)
                self.con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def connectUser(self,userId1,userId2):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "insert into Connections (user_id1,user_id2,conn_st) values(%s,%s,1)"
                args = (userId1, userId2)
                cur.execute(query1,args)
                self.con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def getConnections(self,userId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select u.* from useraccount u, Connections c where (u.user_id=c.user_id1 or u.user_id=c.user_id2)" \
                         " and (c.user_id1 = %s or c.user_id2 =%s) and u.user_id!=%s"
                args = (userId,userId,userId)
                cur.execute(query1, args)
                users = cur.fetchall()
                print(users)

                return users
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def getConnectionsIDs(self, userId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select user_id1 from connections where user_id2 =%s;"
                args = (userId)
                cur.execute(query1, args)
                users1 = cur.fetchall()
                print(users1)

                query2 = "select user_id2 from connections where user_id1 =%s;"
                args = (userId)
                cur.execute(query2, args)
                users2 = cur.fetchall()
                print(users2)
                list2=users1+users2
                listId=[]
                for id in list2:
                    listId.append(id[0])

                listId=list(set(listId))
                print("final connects -=>",list2)
                print("final connects idd -=>", listId)

                return listId
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def getNotesCategories(self):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select notes_subject from notes"
                cur.execute(query1)
                catg = cur.fetchall()
                list2=[]
                for data in catg:
                    list2.append(data[0])
                list2=list(set(list2))
                print("list --> ",list2)
                return list2
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def getSpecificNotes(self,subName,userId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 =  "select notes_title,notes_subject,notes_content,nt_date_created,notes_id,file_uploaded from notes where notes_publicSt=1 and notes_subject=%s;"
                conIds=self.getConnectionsIDs(userId)
                print("connections - ",conIds)
                args=(subName)
                cur.execute(query1,args)
                listNotes1 = cur.fetchall()

                #listNotes1=listNotes1[0]
                listNotes1=list((listNotes1))
                print("list1 --> ", listNotes1)

               # query2 = "select notes_title,notes_subject,notes_content,nt_date_created,notes_id from notes where notes_subject=%s and user_id in (%s);"

                for id in conIds:
                    query2 = "select notes_title,notes_subject,notes_content,nt_date_created,notes_id,file_uploaded from notes where " \
                             "notes_subject=%s and user_id=%s;"
                    args=(subName,id)
                    cur.execute(query2, args)
                    listNotes2 = cur.fetchall()
                    if(len(listNotes2)>0):
                        listNotes1.append(listNotes2[0])


                listNotes = list(set(listNotes1));
                #listNotes=filter(None,listNotes)
                print("list --> ", listNotes)

                return listNotes
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def addTodoList(self,tdObj):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "insert into TodoList(user_id,tl_title,tl_desc,user_name) values(%s,%s,%s,%s);"
                args = (tdObj.td_uId,tdObj.td_title,tdObj.td_desc,tdObj.td_uname)
                cur.execute(query1, args)
                self.con.commit()

                query2 = "update TodoList set tl_id=concat(tl_str,tl_no);"
                cur.execute(query2)
                self.con.commit()


        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def getTodoList(self,userId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                print("User Id in get is : ",userId)
                query1 = "select tl_id,tl_title,tl_desc,user_name from TodoList where user_id=%s"
                args=(userId)
                cur.execute(query1,args)
                list1 = cur.fetchall()
                print("list is : ",list1)
                return list1
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def deleteTodo(self,tdId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "delete from TodoList where tl_id=%s;"
                args = (tdId)
                cur.execute(query1, args)
                self.con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()



    def addNotesFile(self, userId, file1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "UPDATE notes SET file_uploaded=%s WHERE user_id=%s;"
                args = (file1, userId)
                cur.execute(query, args)
                self.con.commit()
                print("file notes added")
                return True
            else:
                print("---AddingProfilePictureFailed---")
                return False
        except Exception as e:
            print("Exception in inserting profile Picture", str(e))
            print("---AddingProfilePictureFailed---")
            return False
        finally:
            if cur != None:
                cur.close()


    def getUserImage(self, userid):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query = "SELECT user_img_path from useraccount where user_id=%s;"
                args = (userid)
                cur.execute(query, args)
                x = cur.fetchall()
                print(x)
                self.con.commit()
                print("getting user image")
                print("img is --> ", x)

                if x == None or x == "" or len(x) == 0:
                    return "usericon.png"
                return x[0][0]

        except Exception as e:
            print("Exception in inserting profile Picture in notification", str(e))
            return False
        finally:
            if cur != None:
                cur.close()


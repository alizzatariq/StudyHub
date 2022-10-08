
class User:
    def __init__(self,name1="",email1="",password1="",acc_type1=""):

        self.name=name1
        self.email=email1
        self.password=password1
        self.acc_type=acc_type1


class Profile:
    def __init__(self,fname,lname,email,password,bio,dob,phoneNo,country,uniName,degree,gender,piclink,userId):
        self.fname=fname
        self.lname=lname
        self.password=password
        self.bio=bio
        self.email=email
        self.dob=dob
        self.phoneNo=phoneNo
        self.country=country
        self.uniName=uniName
        self.degree=degree
        self.gender=gender
        self.piclink = piclink
        self.userId=userId


class TodoList:
    def __init__(self,td_id="",td_uId="",td_date="",td_title="",td_desc="",td_uname=""):
        self.td_id=td_id
        self.td_uId=td_uId
        self.td_date=td_date
        self.td_title=td_title
        self.td_desc=td_desc
        self.td_uname = td_uname

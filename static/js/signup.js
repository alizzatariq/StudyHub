function checkUserName(objName)
{
  if(objName.value.length==0)
  {
    document.getElementById("un").innerHTML="Enter Your Name"
    return false;
  }

  if(objName.value.length>100)
  {
    document.getElementById("un").innerHTML="Maximum 100 characters are allowed.";
    return false;

  }

  var letters=/^[A-Za-z][A-Za-z ]+$/
  console.log(objName.value.match(letters));
  console.log(objName.value)
  if(objName.value.match(letters))
  {
    document.getElementById("un").innerHTML="";
    return true;
  }
  else{
    document.getElementById("un").innerHTML="Incorrect Name Format";
    return false;
  }
}


function checkEmail(objEmail)
{
  if(objEmail.value.length==0)
  {
    document.getElementById("em").innerHTML="Enter Email"
    return false;
  }
  var mail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if(objEmail.value.match(mail))
  {
    document.getElementById("em").innerHTML="";
    return true;
  }
  else
  {
    document.getElementById("em").innerHTML="Incorrect Email format";
    return false;
  }
}



function checkPwd(objPwd)
{
  if(objPwd.value.length==0)
  {
    document.getElementById("pwdErr").innerHTML="Enter Password!"
    return false;
  }
  if(objPwd.value.length<10)
  {
    document.getElementById("pwdErr").innerHTML="Password should be maximum 10 characters"
    return false;
  }

  var pwd=/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{10,}/

  if(objPwd.value.match(pwd))
  {

    document.getElementById("pwdErr").innerHTML=""
    if(document.getElementById("floatingPassword1").value==document.getElementById("floatingPassword2").value)
    {
      document.getElementById("pwdErr1").innerHTML=""
    }
    return true;

  }
  else{
    document.getElementById("pwdErr").innerHTML="Password should contain one Capital Letter,one Small Letter, one Numeric value and one special character"
    return false;

  }

}


function confirmPassword(objPwd)
{

  objPwd1=document.getElementById("floatingPassword1").value;
  if(objPwd.value.length==0)
  {
    document.getElementById("pwdErr1").innerHTML="Enter Password!"
    return false;
  }
  if(objPwd.value.length<10)
  {
    document.getElementById("pwdErr1").innerHTML="Password should be maximum 10 characters"
    return false;
  }

  var pwd=/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{10,}/

  if(objPwd.value.match(pwd))
  {
    if(objPwd.value==objPwd1)
    {
    document.getElementById("pwdErr1").innerHTML=""
    return true;
    }
    else
    {
    document.getElementById("pwdErr1").innerHTML="Password should be same"
    return false;
    }
  }
  else{
    document.getElementById("pwdErr1").innerHTML="Password should contain one Capital Letter,one Small Letter, one Numeric value and one special character"
    return false;

  }
}

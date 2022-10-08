$(document).ready(function(){
    $("#myBtn").click(function(){
        $("#myAlert").alert("close");
    });
});
function removeExtraSpaces()
{
        console.log("Hello world")
    var text1=document.getElementById("content1").value
    let newText=text1.replace(/\s+/g, ' ').trim()
    document.getElementById("content1").value=newText;


}

function coptText()
{
     var text1=document.getElementById("content1").value
    text1.select
    navigator.clipboard.writeText(text1)

}

function upperCase()
{
    var text1=document.getElementById("content1").value
    let newText=text1.toUpperCase()
    document.getElementById("content1").value=newText;
}

function lowerCase()
{
    var text1=document.getElementById("content1").value
    let newText=text1.toLowerCase()
    document.getElementById("content1").value=newText;
}

function clearAll()
{
    var text1=document.getElementById("content1").value
    let newText=""
    document.getElementById("content1").value=newText;
}

function titleCase()
{
       var text1=document.getElementById("content1").value

  text1 = text1.toLowerCase().split(' ');
  for (var i = 0; i < text1.length; i++)
  {
    text1[i] = text1[i].charAt(0).toUpperCase() + text1[i].slice(1);
  }
  let newText=text1.join(' ');
  document.getElementById("content1").value=newText;

}

function toggleCase() {
    var text1 = document.getElementById("content1").value
    let text2=""

    for (var i = 0; i < text1.length; i++) {
        if (text1[i] == text1[i].toUpperCase()) {
           text2= text2+ text1[i].toLowerCase()
        }
        else if (text1[i] == text1[i].toLowerCase()) {
            text2= text2+ text1[i].toUpperCase()
        }
        else
        {
             text2= text2+ text1[i]
        }
    }
    console.log(text2)
    document.getElementById("content1").value = text2;
}
$(document).ready(function(){
    $("#myBtn").click(function(){
        $("#myAlert").alert("close");
    });
});

function readURL(input) {
  if (input.files && input.files[0]) {
    document.getElementById("fileErr").innerHTML=""
      var reader = new FileReader();

      reader.onload = function (e) {
          $('#userPic')
              .attr('src', e.target.result).width(400).height(300);
      };

      reader.readAsDataURL(input.files[0]);
      return true;
  }
  else{
    document.getElementById("fileErr").innerHTML="Upload our Picture Here!"
    return false;
  }
}

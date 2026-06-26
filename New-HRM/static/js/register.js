const password=document.getElementById("password");

const confirm=document.getElementById("confirm_password");

confirm.addEventListener("keyup",()=>{

if(password.value!==confirm.value){

confirm.style.border="2px solid red";

}

else{

confirm.style.border="2px solid green";

}

});
window.addEventListener('load', passwordChecker);


function passwordChecker()
{
    var match = true;
    var valid = false;
    var length = 0;
    var strength = 0;

    var sub = document.getElementById("passwordSubmit");
    var regex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])");
    var pass = document.getElementById("newPassword").value;
    var confPass = document.getElementById("newPasswordAgain").value;
    var below = document.getElementById("bottomText");
    var bar = document.getElementById("passwordBar");
    length = pass.length;

    if(pass != confPass)
        match = false;

    if(regex.test(pass))
        valid = true;

    if(length < 8 || !valid || !match)
        strength = 0;
    else if(length <= 8)
        strength = 1;
    else if(length <= 12)
        strength = 2;
    else if(length <= 16)
        strength = 3;
    else if(length <= 20)
        strength = 4;
    else
        strength = 5;
    console.log(strength);
    console.log(length);
    var text = "";

    if(!match)
        text += "Passwords do not match <br>"
    if(!valid)
        text += "Password must contain Caps AND Special Characters<br>";
    if(length < 8)
        text += "Password must be at least 8 characters<br>";
    else if(length >= 20)
        text += "There's no way you're gonna remember that, be honest with yourself<br>";

    switch(strength)
    {
        case 1:
            bar.style.width = "30%";
            bar.style.background = "#ed0000";
            below.style.color = "#FF0000";
            break;
        case 2:
            bar.style.width = "60%";
            bar.style.background = "#fff700";
            text = "Your password is OK, but it could be better";
            below.style.color = "#fff700";
            break;
        case 3:
            bar.style.width = "80%";
            bar.style.background = "#00f020";
            text = "Your password is strong";
            below.style.color = "#2AE82A";
            break;
        case 4:
            bar.style.width = "100%";
            bar.style.background = "#00f020";
            text = "Your password is very strong!";
            below.style.color = "#2AE82A";
            break;
        default:
            bar.style.width = "10%";
            bar.style.background = "#ed0000";
            below.style.color = "#FF0000";
            break;
    }

    below.innerHTML = text;
console.log(strength);
    if(!valid || strength == 0 || strength == 5)
    {

        sub.disabled = true;
    }
    else
    {

        sub.disabled = false;
    }
}

function disable(id)
{
    document.getElementById(id).disabled = true;
    document.getElementById("oldPassword").value = "";
    document.getElementById("newPassword").value = "";
    document.getElementById("newPasswordAgain").value = "";
    setTimeout(function(){document.getElementById(id).disabled = false;},1000);
    var below = document.getElementById("bottomText");
    below.innerHTML = "Proccessing...";
    setTimeout(passwordChecker,1000);
}
window.onload = onLoadFunctions;

document.addEventListener("scroll", updateLogos)
window.addEventListener("resize", updateLogos)

function updateLogos()
{
    document.getElementById("collapsedLogo").hidden =
        (document.documentElement.scrollTop < document.getElementById("banner").offsetHeight);
    if(document.getElementById("banner").offsetHeight == 0)
        document.getElementById("collapsedLogo").hidden = true;
}

function randomizePfp()
{
    document.getElementById("pfp").src = "assets/img/platypus" + (Math.floor(Math.random()*4)) + ".png";
}

function choosePfp()
{

}

function onLoadFunctions() {
    updateLogos();
    //randomizePfp();
}

function openNav() {
    document.getElementById("mobileMenu").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mobileMenu").style.width = "0";
}
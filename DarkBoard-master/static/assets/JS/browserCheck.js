window.addEventListener('load', browserCheck);

function browserCheck()
{
    if (navigator.appName == 'Microsoft Internet Explorer' ||  !!(navigator.userAgent.match(/Trident/) || navigator.userAgent.match(/rv:11/)) || (typeof $.browser !== "undefined" && $.browser.msie == 1))
    {
        window.location.href = 'errorie.html';
    }
}
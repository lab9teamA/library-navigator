$(document).ready(() => alert("Working"));


function loadDoc() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        // console.log(this.responseText);
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById("test").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "../../static/ajaxtest.txt", true);
    xhttp.send();
}


// $(document).ready(function(){
//     alert("Working");
// });

function loadDoc() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        // console.log(this.responseText);
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById("test").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "http://localhost:8000/libnav/put/", true);
    xhttp.send();
}

let current_floor = 1;
const nFloors = 12;

$(document).ready(() => {
    updateImage(current_floor);
    genList();
});


function genList() {

    const ul = document.getElementById("floorList");
    ul.innerHTML = "";

    const upA = document.createElement("li");
    upA.id = "arrow-up";
    upA.onclick = onArrowUp;

    const downA = document.createElement("li");
    downA.id = "arrow-down";
    downA.onclick = onArrowDown;


    for (let i = nFloors; i > 0; i--) {
        const li = document.createElement("li");
        li.textContent = i.toString();
        li.onclick = onFloorClick;
        if (i === current_floor) {
            if (i !== nFloors)
                ul.appendChild(upA)
            ul.appendChild(li);
            if (i !== 1)
                ul.appendChild(downA)
        } else {
            ul.appendChild(li)
        }

    }
}


function updateImage(new_floor) {
    let url = "http://127.0.0.1:8000/libnav/updatemap/" + new_floor
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        // console.log(this.responseText);
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.responseText);
            let floor = JSON.parse(this.responseText);
            updatePage(floor);
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}


function updatePage(floor) {
    let floor_div = document.getElementById("imageLoc");
    console.log(floor_div.children);
    floor_div.children[0].src = floor.mediaUrl + "floorplans/" + floor.mapName;
    floor_div.children[0].alt = "Level " + floor.number + " Floorplan";
    sessionStorage.setItem("floornum", floor.number);
    sessionStorage.setItem("floorimg", floor.mapName);
}


function onFloorClick(e) {
    current_floor = parseInt(e.target.innerHTML);
    updateImage(current_floor);
    genList();
}


function onArrowUp() {
    current_floor += 1;
    updateImage(current_floor);
    genList();
}

function onArrowDown() {
    current_floor -= 1;
    updateImage(current_floor);
    genList();
}




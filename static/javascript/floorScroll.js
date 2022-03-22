const nFloors = 12;

$(document).ready(() => {
    getCurrentFloor();
    updateImage(current_floor);
    genList();
});


function getCurrentFloor() {
    let url = "http://127.0.0.1:8000/libnav/getcurrentfloor"
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let floor = JSON.parse(this.responseText);
            current_floor = parseInt(floor.floor_number);
        }
    };
    xhttp.open("GET", url, false);
    xhttp.send();
}


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
            let floor = JSON.parse(this.responseText);
            updatePage(floor);
        }
    };
    xhttp.open("GET", url, false);
    xhttp.send();
}


function updatePage(floor) {
    floorimg = floor.mapName;
    floornum = floor.number;
    mediaUrl = floor.mediaUrl
    drawMap();
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




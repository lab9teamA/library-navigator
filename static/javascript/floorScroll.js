let current = 1;
const nFloors = 12

$(document).ready(() => {
    genList();
    // updateImage();
});


function genList() {
    const ul = document.getElementById("floorList");
    ul.innerHTML = "";

    const upA = document.createElement("li");
    upA.className = "arrow-up";
    upA.onclick = onArrowUp;

    const downA = document.createElement("li");
    downA.className = "arrow-down";
    downA.onclick = onArrowDown;


    for (let i = 1; i < nFloors + 1; i++) {
        const li = document.createElement("li");
        li.textContent = i;
        li.onclick = onFloorClick;
        if (i === current) {
            if (i !== 1)
                ul.appendChild(upA)
            ul.appendChild(li);
            if (i !== nFloors)
                ul.appendChild(downA)
        } else {
            ul.appendChild(li)
        }

    }
}

function onFloorClick(e) {
    current = parseInt(e.target.innerHTML);
    genList();
    // updateImage();
}


function onArrowUp() {
    current -= 1;
    genList();
    // updateImage();
}

function onArrowDown() {
    current += 1;
    genList();
    // updateImage();
}




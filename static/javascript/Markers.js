var canvas;
var canvasHeight;
var canvasWidth;
var context;
var friendSprite;
var randomSprite;
var markerSpritePublic;
var markerSpritePrivate;


$(document).ready(() => {
    current_floor = parseInt(document.getElementById("floor_number").textContent);
    updateImage(current_floor);
    drawSetUp();
});

function updateImage(new_floor) {
    let url = "http://127.0.0.1:8000/libnav/updatemap/" + new_floor
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let floor = JSON.parse(this.responseText);
            updatePage(floor);
        }
    };
    xhttp.open("GET", url, false);
    xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhttp.send();
}

function updatePage(floor) {
    floorimg = floor.mapName;
    floornum = floor.number;
    mediaUrl = floor.mediaUrl
}

var Marker = function () {
    this.Width = 20;
    this.Height = 20;
    this.XPos = 0;
    this.YPos = 0;
}

var Markers = new Array();


function drawMap() {
    try {
        context.clearRect(0, 0, canvasWidth, canvasHeight);
    }catch(e){
        //nothing
    }
    var src = mediaUrl + "floorplans/" + floorimg;

    // Map sprite
    var mapSprite = new Image();
    mapSprite.src = mediaUrl + "floorplans/" + floorimg;

    var locmap = {};
    var text;
    var measurements

    const getLocUrl = new URL("http://127.0.0.1:8000/libnav/api/get-loc/")
    const user = JSON.parse(document.getElementById('user-id').textContent);
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            locmap = JSON.parse(this.responseText);
            locmap["friends"] = [{"x": 1100, "y": 500, "name": "Duncan"}, {"x": 400, "y": 300, "name": "Jahan"}, {"x": 550, "y": 350, "name": "David"}, {"x": 650, "y": 500, "name": "Leo"}];
            locmap["others"] = [{"x": 300, "y": 300}, {"x": 400, "y": 400}];
            mapSprite.onload = function () {
                context.drawImage(mapSprite, 0, 0, canvasWidth, canvasHeight);
                for (let i = 0; i < locmap["others"].length; i++) {
                    context.drawImage(randomSprite, locmap["others"][i]["x"], locmap["others"][i]["y"], 18, 22);
                }
                for (let i = 0; i < locmap["friends"].length; i++) {
                    text = locmap["friends"][i]["name"];
                    measurements = context.measureText(text);
                    context.fillStyle = "#000000";
                    context.globalAlpha = 0.8;
                    context.fillRect(locmap["friends"][i]["x"] - (measurements.width/20)-2, locmap["friends"][i]["y"] - 10, measurements.width+4, 15);
                    context.globalAlpha = 1;
                    context.fillStyle = "#ffffff";
                    context.fillText(text, locmap["friends"][i]["x"]-1, locmap["friends"][i]["y"]);
                    context.drawImage(friendSprite, locmap["friends"][i]["x"], locmap["friends"][i]["y"]+5, 18, 22);
                }
                if (locmap["user_loc"].length > 0) {
                    text = "You";
                    measurements = context.measureText(text);
                    context.fillStyle = "#000000";
                    context.globalAlpha = 0.8;
                    context.fillRect(locmap["user_loc"][0]["x"] - (measurements.width/20)-2, locmap["user_loc"][0]["y"] - 10, measurements.width+4, 15);
                    context.globalAlpha = 1;
                    context.fillStyle = "#ffffff";
                    context.fillText(text, locmap["user_loc"][0]["x"]-1, locmap["user_loc"][0]["y"]);
                    console.log(text);
                    drawMarker(locmap["user_loc"][0]["x"], locmap["user_loc"][0]["y"]+5, locmap["user_loc"][0]["private"]);
                }
            }
        }
    };
    getLocUrl.searchParams.set("userID", user)
    getLocUrl.searchParams.set("floor", floornum)
    xhttp.open("GET", getLocUrl, false);
    xhttp.send();
}

function drawMarker(xpos, ypos, private) {
    if (private) {
        // Draw marker
        context.drawImage(markerSpritePrivate, xpos, ypos, 18, 22);
    } else {
        // Draw marker
        context.drawImage(markerSpritePublic, xpos, ypos, 18, 22);
    }
}


function deleteMarker(user) {
    const deleteMarkerUrl = new URL("http://127.0.0.1:8000/libnav/api/remove-loc/");
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log("Marker deleted");
        }
    };
    let post_data = {"userID": user}
    xhttp.open("POST", deleteMarkerUrl, false);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(post_data));
}


function mouseClicked (mouse) {
    var user = JSON.parse(document.getElementById('user-id').textContent);

    // clicking should only do anything when user is logged in
    if (user != null) {
        // Get current mouse coords
        var rect = canvas.getBoundingClientRect();
        var mouseXPos = (mouse.x - rect.left);
        var mouseYPos = (mouse.y - rect.top);

        // Move the marker when placed to a better location
        var m = new Marker();
        m.XPos = mouseXPos - (m.Width / 2);
        m.YPos = mouseYPos - m.Height;

        // check if existing marker has been clicked, if yes, ask if it should be deleted
        var marker_clicked = false;
        const getLocUrl = new URL("http://127.0.0.1:8000/libnav/api/get-loc/");
        const xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                var locmap = JSON.parse(this.responseText);
                if (locmap["user_loc"].length > 0) {
                    var user_loc = locmap["user_loc"][0]
                    if (mouseXPos > user_loc["x"] && mouseXPos < (user_loc["x"]+20)) {
                        if (mouseYPos > user_loc["y"] && mouseYPos < (user_loc["y"]+26)) {
                            marker_clicked = true;
                            if (window.confirm("Delete marker?")){
                                deleteMarker(user);
                            }
                        }
                    }
                }
            }
        }
        getLocUrl.searchParams.set("userID", user);
        getLocUrl.searchParams.set("floor", floornum);
        xhttp.open("GET", getLocUrl, false);
        xhttp.send();

        // if marker hasn't been clicked, i.e somewhere else on page clicked, move marker
        if (!marker_clicked) {
            if (window.confirm("Make marker public?")) {
                var private = false;
                drawMarker(m.XPos, m.YPos, private);
            } else {
                var private = true;
                drawMarker(m.XPos, m.YPos, private);
            }

            const setLocUrl = new URL("http://127.0.0.1:8000/libnav/api/set-loc/");
            const xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState === 4 && this.status === 200) {
                    console.log("location set");
                }
            };
            let post_data = {"userID": user, "x": m.XPos, "y": m.YPos, "floor": floornum, "private": private}
            xhttp.open("POST", setLocUrl, false);
            xhttp.setRequestHeader("Content-type", "application/json");
            xhttp.send(JSON.stringify(post_data));
        }

        drawMap();
    }
}




function drawSetUp() {
    canvas = document.getElementById('canvas');
    context = canvas.getContext("2d");
    context.font = "15px Georgia";
    context.textAlign = "center";
    // Add mouse click event listener to canvas
    canvas.addEventListener("mousedown", mouseClicked, false);

    // get height and width for canvas
    var containerDiv = document.getElementById("mainbody")
    canvasHeight = containerDiv.offsetHeight-100;
    canvasWidth = containerDiv.offsetWidth-100;
    canvas.height = canvasHeight;
    canvas.width = canvasWidth;

    friendSprite = new Image();
    friendSprite.onload = function(){}
    friendSprite.src = mediaUrl + "map_pins/friendpin.png";
    //friendSprite.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Map_pin_icon_green.svg/1504px-Map_pin_icon_green.svg.png";
    randomSprite = new Image();
    randomSprite.onload = function(){}
    randomSprite.src = mediaUrl + "map_pins/randompin.png";
    //randomSprite.src = "https://img.favpng.com/20/11/24/google-map-maker-google-maps-computer-icons-map-collection-png-favpng-BNWkuCw9tdsBqxLR2PTzGbS6V.jpg";
    markerSpritePublic = new Image();
    markerSpritePublic.onload = function(){}
    markerSpritePublic.src = mediaUrl + "map_pins/userpin.png";
    //markerSpritePublic.src = "https://www.pinclipart.com/picdir/middle/126-1269086_google-map-marker-red-peg-png-image-red.png";
    markerSpritePrivate = new Image()
    markerSpritePrivate.onload = function(){}
    markerSpritePrivate.src = mediaUrl + "map_pins/privatepin.png"
    //markerSpritePrivate.src = "https://cdn-icons-png.flaticon.com/512/446/446075.png";

    drawMap();

};
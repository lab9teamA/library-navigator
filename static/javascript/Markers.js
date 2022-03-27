var canvas;
var canvasHeight;
var canvasWidth;
var context;
var friendSprite;
var randomSprite;
var markerSpritePublic;
var markerSpritePrivate;
var markerWidth = 18;
var markerHeight = 22;
var floorimg;
var current_floor;
var mediaUrl;


$(document).ready(() => {
    current_floor = parseInt(document.getElementById("floor_number").textContent);
    floorimg = JSON.parse(document.getElementById('floor_map').textContent);
    mediaUrl = JSON.parse(document.getElementById('media_url').textContent);
    drawSetUp();
});


var Marker = function () {
    this.Width = 20;
    this.Height = 20;
    this.XPos = 0;
    this.YPos = 0;
}

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
            mapSprite.onload = function () {
                context.drawImage(mapSprite, 0, 0, canvasWidth, canvasHeight);
                for (let i = 0; i < locmap["others"].length; i++) {
                    context.drawImage(randomSprite, locmap["others"][i]["x"], locmap["others"][i]["y"], markerWidth, markerHeight);
                }
                for (let i = 0; i < locmap["friends"].length; i++) {
                    text = locmap["friends"][i]["name"];
                    measurements = context.measureText(text);
                    context.fillStyle = "#000000";
                    context.globalAlpha = 0.8;
                    context.fillRect(locmap["friends"][i]["x"]-(measurements.width-markerWidth+4)/2, locmap["friends"][i]["y"]-10, measurements.width+4, 15);
                    context.globalAlpha = 1;
                    context.fillStyle = "#ffffff";
                    context.fillText(text, locmap["friends"][i]["x"]-(measurements.width-markerWidth)/2, locmap["friends"][i]["y"]);
                    context.drawImage(friendSprite, locmap["friends"][i]["x"], locmap["friends"][i]["y"]+5, markerWidth, markerHeight);
                }
                if (locmap["user_loc"].length > 0) {
                    text = "You";
                    measurements = context.measureText(text);
                    context.fillStyle = "#000000";
                    context.globalAlpha = 0.8;
                    context.fillRect(locmap["user_loc"][0]["x"] - (measurements.width-markerWidth+4)/2, locmap["user_loc"][0]["y"] - 10, measurements.width+4, 15);
                    context.globalAlpha = 1;
                    context.fillStyle = "#ffffff";
                    context.fillText(text, locmap["user_loc"][0]["x"]-(measurements.width-markerWidth)/2, locmap["user_loc"][0]["y"]);
                    drawMarker(locmap["user_loc"][0]["x"], locmap["user_loc"][0]["y"]+5, locmap["user_loc"][0]["private"]);
                }
            }
        }
    };
    getLocUrl.searchParams.set("userID", user)
    getLocUrl.searchParams.set("floor", current_floor)
    xhttp.open("GET", getLocUrl, false);
    xhttp.send();
}

function drawMarker(xpos, ypos, private) {
    if (private) {
        // Draw marker
        context.drawImage(markerSpritePrivate, xpos, ypos, markerWidth, markerHeight);
    } else {
        // Draw marker
        context.drawImage(markerSpritePublic, xpos, ypos, markerWidth, markerHeight);
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
        getLocUrl.searchParams.set("floor", current_floor);
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
                    console.log("Location set");
                }
            };
            let post_data = {"userID": user, "x": m.XPos, "y": m.YPos, "floor": current_floor, "private": private}
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
    randomSprite = new Image();
    randomSprite.onload = function(){}
    randomSprite.src = mediaUrl + "map_pins/randompin.png";
    markerSpritePublic = new Image();
    markerSpritePublic.onload = function(){}
    markerSpritePublic.src = mediaUrl + "map_pins/userpin.png";
    markerSpritePrivate = new Image()
    markerSpritePrivate.onload = function(){}
    markerSpritePrivate.src = mediaUrl + "map_pins/privatepin.png"

    drawMap();

};
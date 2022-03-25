var canvas;
var canvasHeight;
var canvasWidth;
var context;
var friendSprite;
var randomSprite;
var markerSpritePublic;
var markerSpritePrivate;




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

    const getLocUrl = new URL("http://127.0.0.1:8000/libnav/api/get-loc/")
    const user = JSON.parse(document.getElementById('user-id').textContent);
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            locmap = JSON.parse(this.responseText);
            //locmap["friends"] = [{"x": 100, "y": 100}, {"x": 200, "y": 200}, {"x": 250, "y": 100}, {"x": 150, "y": 500}];
            //locmap["others"] = [{"x": 300, "y": 300}, {"x": 400, "y": 400}];
            mapSprite.onload = function () {
                context.drawImage(mapSprite, 0, 0, canvasWidth, canvasHeight);
                if (locmap["user_loc"].length > 0) {
                    drawMarker(locmap["user_loc"][0]["x"], locmap["user_loc"][0]["y"], locmap["user_loc"][0]["private"]);
                }
                for (let i = 0; i < locmap["friends"].length; i++) {
                    console.log(locmap["friends"][i]["name"]);
                    context.drawImage(friendSprite, locmap["friends"][i]["x"], locmap["friends"][i]["y"], 18, 22);
                }
                for (let i = 0; i < locmap["others"].length; i++) {
                    context.drawImage(randomSprite, locmap["others"][i]["x"], locmap["others"][i]["y"], 18, 22);
                }
            }
            let amount = locmap["friends"].length + locmap["others"].length;
            let busyness = Math.trunc(amount / 5);
            console.log("Busyness: " + busyness);
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


function mouseClicked (mouse) {

    
    // Get current mouse coords
    var rect = canvas.getBoundingClientRect();
    var mouseXPos = (mouse.x - rect.left);
    var mouseYPos = (mouse.y - rect.top);

    // Move the marker when placed to a better location
    var m = new Marker();
    m.XPos = mouseXPos - (m.Width / 2);
    m.YPos = mouseYPos - m.Height;

    //drawMap();
    var user = JSON.parse(document.getElementById('user-id').textContent);
    if(user!=null){
        if (window.confirm("Make marker public?")){
            var private = false;
            drawMarker(m.XPos, m.YPos, private);
        }else{
            var private = true;
            drawMarker(m.XPos, m.YPos, private);
        }
    
        const setLocUrl = new URL("http://127.0.0.1:8000/libnav/api/set-loc/");
        const xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log("Post worked");
            }
        };
        console.log("User id is " + user);
        let post_data = {"userID": user, "x": m.XPos, "y": m.YPos, "floor": floornum, "private": private }
        console.log("Json data: " + JSON.stringify(post_data))
        xhttp.open("POST", setLocUrl, false);
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send(JSON.stringify(post_data));
    
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
    canvasHeight = containerDiv.offsetHeight;
    canvasWidth = containerDiv.offsetWidth;
    canvas.height = canvasHeight;
    canvas.width = canvasWidth;

    friendSprite = new Image();
    friendSprite.onload = function(){}
    friendSprite.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Map_pin_icon_green.svg/1504px-Map_pin_icon_green.svg.png";
    randomSprite = new Image();
    randomSprite.onload = function(){}
    randomSprite.src = "https://img.favpng.com/20/11/24/google-map-maker-google-maps-computer-icons-map-collection-png-favpng-BNWkuCw9tdsBqxLR2PTzGbS6V.jpg";
    markerSpritePublic = new Image();
    markerSpritePublic.onload = function(){}
    markerSpritePublic.src = "https://www.pinclipart.com/picdir/middle/126-1269086_google-map-marker-red-peg-png-image-red.png";
    markerSpritePrivate = new Image()
    markerSpritePrivate.onload = function(){}
    markerSpritePrivate.src = "https://cdn-icons-png.flaticon.com/512/446/446075.png";

    drawMap();

};
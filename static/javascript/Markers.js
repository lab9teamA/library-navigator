var canvas;
var canvasHeight;
var canvasWidth;
var context;
var mapSprite;
var friendSprite;
var randomSprite;




var Marker = function () {
    this.Width = 20;
    this.Height = 20;
    this.XPos = 0;
    this.YPos = 0;
}

var Markers = new Array();


function drawMap() {
    context.clearRect(0,0,canvasWidth,canvasHeight);

    var src = mediaUrl + "floorplans/" + floorimg;

    // Map sprite
    var mapSprite = new Image();
    mapSprite.src = mediaUrl + "floorplans/" + floorimg;

    var friendSprite = new Image();
    friendSprite.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Map_pin_icon_green.svg/1504px-Map_pin_icon_green.svg.png"

    var randomSprite = new Image();
    randomSprite.src = "https://img.favpng.com/20/11/24/google-map-maker-google-maps-computer-icons-map-collection-png-favpng-BNWkuCw9tdsBqxLR2PTzGbS6V.jpg"


    var locmap = {};

    const getLocUrl = new URL("http://localhost:8000/libnav/api/get-loc/")
    const user = JSON.parse(document.getElementById('user-id').textContent);
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            locmap = JSON.parse(this.responseText);
            locmap["friends"] = [[100,100],[200,200],[250,100],[150,500]];
            locmap["others"] = [[300,300],[400,400]];
            mapSprite.onload = function(){
                context.drawImage(mapSprite, 0, 0, canvasWidth, canvasHeight);
                for(let i=0; i<locmap["friends"].length;i++){
                        context.drawImage(friendSprite, locmap["friends"][i][0], locmap["friends"][i][1],20,20);
                }
                for(let i=0; i<locmap["others"].length;i++){
                        context.drawImage(randomSprite, locmap["others"][i][0], locmap["others"][i][1],20,20);
                }
            }
            let amount = locmap["friends"].length+locmap["others"].length;
            let busyness = Math.trunc(amount/5);
            console.log(busyness);    
        }
    };
    getLocUrl.searchParams.set("userID", user)
    xhttp.open("GET", getLocUrl, true);
    xhttp.send();


    //draw other peoples markers on this floor
    

    
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
    console.log(context);

    drawMap();

    if (window.confirm("Make marker public?")){

        var private = true;
    	var markerSprite = new Image();
		markerSprite.src = "https://www.pinclipart.com/picdir/middle/126-1269086_google-map-marker-red-peg-png-image-red.png"
    
    	// Move the marker when placed to a better location
    	var m = new Marker();
    	m.XPos = mouseXPos - (m.Width / 2);
   		m.YPos = mouseYPos - m.Height;
    
   		// Draw marker
        console.log(mouse);
        console.log(m.XPos, m.YPos, m.Width, m.Height);
        markerSprite.onload = function() {
            context.drawImage(markerSprite, m.XPos, m.YPos, m.Width, m.Height);
        };
        console.log(m);
        console.log(context);

    }else{
        
        var private = false;
    	var markerSprite = new Image();
		markerSprite.src = "https://silicondales.com/wp-content/uploads/2018/11/incognito-symbol-large.jpg"
    
    	// Move the marker when placed to a better location
    	var m = new Marker();
    	m.XPos = mouseXPos - (m.Width / 2);
   		m.YPos = mouseYPos - m.Height;
    
   		// Draw marker
        markerSprite.onload = function() {
            context.drawImage(markerSprite, m.XPos, m.YPos, m.Width, m.Height);
        };
    
    }

    const setLocUrl = new URL("http://localhost:8000/libnav/api/set-loc/")
    const user = JSON.parse(document.getElementById('user-id').textContent);
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            JSON.stringify({"x": m.XPos, "y": m.YPos, "floor": floornum, "private": private });
        }
    };
    setLocUrl.searchParams.set("userID", user)
    xhttp.open("POST", setLocUrl, true);
    xhttp.send();

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

    drawMap();

};
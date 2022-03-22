var canvas;
var canvasHeight;
var canvasWidth;
var context;
var mapSprite;
var friendSprite;
var randomSprite;


var friendSprite = new Image();
friendSprite.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Map_pin_icon_green.svg/1504px-Map_pin_icon_green.svg.png"

var randomSprite = new Image();
randomSprite.src = "https://www.clipartmax.com/png/middle/69-696141_map-pointer-map-marker-icon.png"


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
    // Draw map
    mapSprite.onload = function() {
        context.drawImage(mapSprite, 0, 0, canvasWidth, canvasHeight);
    };

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        console.log(this.responseText);
        if (this.readyState === 4 && this.status === 200) {
            //let locmap = JSON.parse(this.responseText);
            console.log(this.responseText);
        }
    };
    xhttp.open("GET", "http://localhost:8000/libnav/api/get-loc/", true);
    xhttp.send();


    //draw other peoples markers on this floor
    // mapSprite.onload = function(){
    //     for(let i=0; i<locmap["friends"].length;i++){
    //         context.drawImage(friendSprite, locmap["friends"][i].x, locmap["friends"][i].y,20,20);
    //     }
    //     for(let i=0; i<locmap["others"].length;i++){
    //         context.drawImage(randomSprite, locmap["others"][i].x, locmap["others"][i].y,20,20);
    //     }
    // }

    
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

    //const xhttp = new XMLHttpRequest();
    //xhttp.onreadystatechange = function () {
        //console.log(this.responseText);
        //if (this.readyState === 4 && this.status === 200) {
            //JSON.stringify(m.XPos,m.YPos);
        //}
    //};
    //xhttp.open("POST", "http://localhost:8000/libnav/get-loc/", true);
    //xhttp.send();

}




window.onload = function () {
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
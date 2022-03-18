var canvas = document.getElementById('canvas');
var context = canvas.getContext("2d");

//const xhttp = new XMLHttpRequest();
//xhttp.onreadystatechange = function () {
        // console.log(this.responseText);
  //      if (this.readyState === 4 && this.status === 200) {
    //        document.getElementById("map").innerHTML = this.responseText;
      //  }
//};
//xhttp.open("GET", "http://localhost:8000/libnav/put/", true);
//xhttp.send();

var floornum = sessionStorage.getItem("floornum");
var floorimg = sessionStorage.getItem("floorimg");

// Map sprite
var mapSprite = new Image();
mapSprite.src = floorimg;

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

var mouseClicked = function (mouse) {

    
    // Get current mouse coords
    var rect = canvas.getBoundingClientRect();
    var mouseXPos = (mouse.x - rect.left);
    var mouseYPos = (mouse.y - rect.top);


    // Move the marker when placed to a better location
    var m = new Marker();
    m.XPos = mouseXPos - (m.Width / 2);
    m.YPos = mouseYPos - m.Height;

    context.clearRect(0,0,700,700);
    window.onload();

    if (window.confirm("Make marker public?")){
    
    	var markerSprite = new Image();
		markerSprite.src = "https://www.pinclipart.com/picdir/middle/126-1269086_google-map-marker-red-peg-png-image-red.png"
    
    	// Move the marker when placed to a better location
    	var m = new Marker();
    	m.XPos = mouseXPos - (m.Width / 2);
   		m.YPos = mouseYPos - m.Height;
    
   		// Draw marker
    	context.drawImage(markerSprite, m.XPos, m.YPos, m.Width, m.Height);

    }else{
    
    	var markerSprite = new Image();
		markerSprite.src = "https://silicondales.com/wp-content/uploads/2018/11/incognito-symbol-large.jpg"
    
    	// Move the marker when placed to a better location
    	var m = new Marker();
    	m.XPos = mouseXPos - (m.Width / 2);
   		m.YPos = mouseYPos - m.Height;
    
   		// Draw marker
    	context.drawImage(markerSprite, m.XPos, m.YPos, m.Width, m.Height);
    
    }

    //const responseFromRequest = await fetch("https://silicondales.com/wp-content/uploads/2018/11/incognito-symbol-large.jpg", {
      //      method: 'POST',
       //     body: JSON.stringify({x: m.XPos, y: m.YPos})
        //}).then((response) => response.json());
    
    
    //Markers.push(m);
}


// Add mouse click event listener to canvas
canvas.addEventListener("mousedown", mouseClicked, false);

var firstLoad = function () {
    context.font = "15px Georgia";
    context.textAlign = "center";
}

firstLoad();

window.onload = function () {
    // Draw map
    context.drawImage(mapSprite, 0, 0, 800, 800);
    //for(let i=0;i<Markers[1].length;i++){
    //    context.drawImage(friendSprite, Markers[1][i].x,Markers[1][i].y,20,20);
    //}
    //for(let i=0;i<Markers[2].length;i++){
    //    context.drawImage(randomSprite, Markers[i].x,Markers[i].y,20,20)
    //}
};
function updateButtons() {
	if(document.getElementById("checkoutButton")) { // in case book is checked out by someone else
		document.getElementById("checkoutButton").hidden = flags.checkout;
		document.getElementById("checkinButton").hidden = !flags.checkout;
	}
	
	document.getElementById("likeButton").hidden = flags.like;
	document.getElementById("unlikeButton").hidden = !flags.like;
	
	document.getElementById("recommendButton").hidden = flags.recommend;
	document.getElementById("unrecommendButton").hidden = !flags.recommend;
};

window.onload = function() {
	updateButtons();
};

// action indicates which button has been pressed
// value indicates whether the action should be done (i.e. add a like, recommend, check out) or undone
function updateBook(action, value) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
			let response = JSON.parse(this.responseText);
			
			switch(action) {
				case 'checkout':
					// set the flag to true (show checkout button) if value is positive (=1)
					flags.checkout = value>0;
					break;
					
				case 'like':
					// update like count
					document.getElementById("likes").innerHTML = response.likes + " like this";
					// set the flag to true (show like button) if value is positive (=1)
					flags.like = value>0;
					break;
					
				case 'recommend':
					// set the flag to true (show recommend button) if value is positive (=1)
					flags.recommend = value>0;
					break;
			}
			// switch visible buttons
			updateButtons();
        }
    };
	var params = "value="+value.toString()+"&action="+action.toString()
    xhttp.open("GET", window.location.href+"update_book/?"+params, true);
    xhttp.send();
}
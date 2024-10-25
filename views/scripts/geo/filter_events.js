// filter state
var FilterState = {
				   "admin-level": "",
				   "granularity": "",
				   "year": "",
				   "sex": "",
				   "zvadzoka": ""
				  };

// validate filters
function validateFilters() {
	if (FilterState["admin-level"] === "") { FilterState["admin-level"] = "ward"; }
	if (FilterState["granularity"] === "") { FilterState["granularity"] = "ward"; }
	if (FilterState["year"] === "") { FilterState["year"] = 2022; }
	if (FilterState["sex"] === "") { FilterState["sex"] = "total"; }
	return true;
}

function adminNamesResponseHandler(event,response) {
	var filterContainer = document.getElementById("admin-names-container");
	var names = JSON.parse(response);
	const key = Object.keys(names)[0];
	var namesElement =  `
						<label for="admin-names">${Object.keys(names)[0][0].toUpperCase() + Object.keys(names)[0].slice(1)}</label>
						<div>
						<select id="admin-names" name="adminNames">
						`;
									  
	for (i=0;i<names[key].length;i++) {
		namesElement += `<option value=${names[key][i]}>${names[key][i]}</option>"`
		console.log(names[key][i]);
	}
	namesElement += "</select>";
	filterContainer.innerHTML += namesElement;
}

// update filter state
function updateFilterState(event) {
	FilterState[event.target.parentNode.attributes[0].nodeValue] = event.target.innerHTML.toLowerCase();
	console.log(FilterState);
}

// update admin-level state
function updateAdminLevelState(event) {
	console.log(FilterState);
	if (FilterState["admin-level"] === event.target.value) { 
		FilterState["admin-level"] = "";
		FilterState["granularity"] = "";
    } 
    else {
    	FilterState[event.srcElement.id] = event.target.value;
    	FilterState["granularity"] = "";
    	console.log(FilterState);
    
		if (event.target.value === "ward") { 
			FilterState["granularity"] = "ward";
			var grain = document.getElementById("grain");
			grain.value = "ward";
			grain.setAttribute("disabled","true");
		}

		if (event.target.value === "district") {
			document.getElementById("grain").removeAttribute("disabled",);
			zvakavanda(event.target.value,adminNamesResponseHandler);
			
		}
		if (event.target.value === "province") {
			document.getElementById("grain").setAttribute("disabled","false");
			
		}
	}
}

// update granularity state
function updateGrainState(event) {
	if (FilterState["admin-level"] === ""){
		console.log("FIRST SELECT Admin Level");
		return;
	}
	grain = event.target.innerHTML.toLowerCase();
	if (FilterState["granularity"] === grain) {
		FilterState["granularity"] = "";
		// unhide or make siblings clickable
	}
	else {
		if (grain === "district") {
			if (FilterState["admin-level"] === "ward") {
				console.log("granularity - district - not possible for admin level - " + FilterState["admin-level"]);
				return;
			}
		}
		if (grain === "province") {
			if ((FilterState["admin-level"] === "ward") || (FilterState["admin-level"] === "district")) {
				console.log("granularity - province not possible for admin level - " + FilterState["admin-level"]);
				return;
			}
		}
		FilterState[event.target.parentNode.attributes[0].nodeValue] = grain;
		// hide or make siblings unclickable
	}
	console.log(FilterState);

}

// Admin Level 
admin = document.getElementById("admin-level");
admin.addEventListener("change",updateAdminLevelState);

//for (i=0;i<3;i++) { admin[i].addEventListener("click", updateAdminLevelState); }

// // Spatial Granularity
// grain = document.getElementsByClassName("granularity");
// for (i=0;i<3;i++) { grain[i].addEventListener("click", updateGrainState); }


// // Year 
// t = document.getElementsByClassName("year");
// for (i=0;i<3;i++) { t[i].addEventListener("click", updateFilterState); }


// // Sex
// sex = document.getElementsByClassName("sex");
// for (i=0;i<2;i++) { sex[i].addEventListener("click", updateFilterState); }


// // apply filters
// dispatcher = document.getElementById("show-label");
// dispatcher.addEventListener("click", () => {
// 											  if (validateFilters()) { tumira(event,FilterState); }
// 										   }
// 							);

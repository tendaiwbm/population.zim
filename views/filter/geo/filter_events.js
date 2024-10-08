// filter state
var FilterState = {
				   "admin-level": "",
				   "granularity": "",
				   "year": "",
				   "sex": "",
				   "zvadzoka": parent.mhinduro
				  };

// validate filters
function validateFilters() {
	if (FilterState["admin-level"] === "") { FilterState["admin-level"] = "ward"; }
	if (FilterState["granularity"] === "") { FilterState["granularity"] = "ward"; }
	if (FilterState["year"] === "") { FilterState["year"] = 2022; }
	if (FilterState["sex"] === "") { FilterState["sex"] = "total"; }
	return true;
}

// update filter state
function updateFilterState(event) {
	FilterState[event.target.parentNode.attributes[0].nodeValue] = event.target.innerHTML.toLowerCase();
	console.log(FilterState);
}

// update admin-level state
function updateAdminLevelState(event) {
	level = event.target.innerHTML.toLowerCase();
	if (FilterState["admin-level"] === level) { 
		FilterState["admin-level"] = "";
		FilterState["granularity"] = "";
		// indicate unclicked	
		// unhide or make clickable siblings
    } 
    else {
    	FilterState[event.target.parentNode.attributes[0].nodeValue] = level;
    	FilterState["granularity"] = "";
    	// indicate clicked
    
		if (level === "ward") { 
			FilterState["granularity"] = "ward";
			// hide the other 2 or make them unclickable
			// indicate clicked
		}
		if (level === "district") {
			// hide province or make unclickable
			// indicate clicked
			parent.zvakavanda(level);
		}
		if (level === "province") {
			// hide province or make unclickable
			// indicate clicked
			parent.zvakavanda(level);
		}
	}
	console.log(FilterState)
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
admin = document.getElementsByClassName("admin-level");
for (i=0;i<3;i++) { admin[i].addEventListener("click", updateAdminLevelState); }

// Spatial Granularity
grain = document.getElementsByClassName("granularity");
for (i=0;i<3;i++) { grain[i].addEventListener("click", updateGrainState); }


// Year 
t = document.getElementsByClassName("year");
for (i=0;i<3;i++) { t[i].addEventListener("click", updateFilterState); }


// Sex
sex = document.getElementsByClassName("sex");
for (i=0;i<2;i++) { sex[i].addEventListener("click", updateFilterState); }


// apply filters
dispatcher = document.getElementById("show-label");
dispatcher.addEventListener("click", () => {
											  if (validateFilters()) { tumira(event,FilterState); }
										   }
							);

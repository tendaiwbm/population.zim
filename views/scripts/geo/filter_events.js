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
						<label id="admin-names-label" for="admin-names">${key[0].toUpperCase() + key.slice(1)}</label>
						<div>
						<select id="admin-names" name="adminNames">
						`;
									  
	for (i=0;i<names[key].length;i++) {
		namesElement += `<option value=${names[key][i]}>${names[key][i]}</option>"`
		console.log(names[key][i]);
	}
	namesElement += "</select>";
	
	if (!document.getElementById("admin-names")) {
		filterContainer.innerHTML += namesElement;
	}
	else {
		document.getElementById("admin-names").innerHTML = namesElement;
		document.getElementById("admin-names-label").innerText = key[0].toUpperCase() + key.slice(1);
	}
}

// update filter state
function updateFilterState(event) {
	FilterState[event.target.parentNode.attributes[0].nodeValue] = event.target.innerHTML.toLowerCase();
	console.log(FilterState);
}

// update admin-level state
function updateAdminLevelState(event) {
	if (FilterState["admin-level"] === event.target.value) { 
		FilterState["admin-level"] = "";
		FilterState["granularity"] = "";
    } 
    else {
    	FilterState[event.srcElement.id] = event.target.value;
    	FilterState["granularity"] = "";
    
		if (event.target.value === "ward") { 
			if (document.getElementById("admin-names")) { 
				document.getElementById("admin-names").remove();
				document.getElementById("admin-names-label").remove(); 
			}
			FilterState["granularity"] = "ward";
			var grain = document.getElementById("grain");
			grain.value = "ward";
			grain.setAttribute("disabled","true");
		}

		else {
			document.getElementById("grain").value = "";
			FilterState["granularity"] = event.target.value;
			zvakavanda(event.target.value,adminNamesResponseHandler);
			document.getElementById("grain").removeAttribute("disabled")
			if (event.target.value === "district") { document.getElementById("grain").getElementsByTagName("option")[3].disabled = true; }
			else if (event.target.value === "province") { document.getElementById("grain").getElementsByTagName("option")[3].disabled = false; } 
		}
	}
}

// update granularity state
function updateGrainState(event) {
	if (FilterState["admin-level"] === ""){
		console.log("FIRST SELECT Admin Level");
		return;
	}
	
	if (event.target.value === "district") {
		if (FilterState["admin-level"] === "ward") {
			console.log("granularity - district - not possible for admin level - " + FilterState["admin-level"]);
			return;
		}
	}
	if (event.target.value === "province") {
		if ((FilterState["admin-level"] === "ward") || (FilterState["admin-level"] === "district")) {
			console.log("granularity - province not possible for admin level - " + FilterState["admin-level"]);
			return;
		}
	}
	FilterState["granularity"] = event.target.value;
	console.log(FilterState);

}

// Admin Level 
admin = document.getElementById("admin-level");
admin.addEventListener("change",updateAdminLevelState);

// Spatial Granularity
grain = document.getElementById("grain");
grain.addEventListener("change", updateGrainState);


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

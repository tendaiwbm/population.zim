// filter state
var FilterState = {
				   "admin-level": "",
				   "granularity": "",
				   "year": "",
				   "sex": "total",
				   "admin-names": [],
				   "zvadzoka": mhinduro
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
	// var namesElement =  `
	// 					<label id="admin-names-label" for="admin-names">${key[0].toUpperCase() + key.slice(1)}</label>
	// 					<div>
	// 					<select id="admin-names" name="adminNames">
	// 						<option value=""></option>
	// 					`;
	var namesElement = `
	 					<label id="admin-names-label">${key[0].toUpperCase() + key.slice(1)}</label>
	 					<div>
	 						<div id="admin-names-dummy-searchable">
	 							<input id="admin-name-search" type="search" size=21 />
	 							<img id="admin-names-dropdown" src="images/dropdown.png" />
	 						</div>
	 						<div id="admin-names">
					   `;

	for (i=0;i<names[key].length;i++) {
		namesElement += `<div><input type="checkbox" class="admin-options" name="${names[key][i].toLowerCase()}"/><label for="${names[key][i].toLowerCase()}">${names[key][i]}</label></div>`;
	}
	namesElement += "</div></div>";

	// for (i=0;i<names[key].length;i++) {
	// 	namesElement += `<option value=${names[key][i]}>${names[key][i]}</option>"`
	// }
	// namesElement += "</select>";
	
	if (!document.getElementById("admin-names")) {
		filterContainer.innerHTML += namesElement;
	}
	else {
		document.getElementById("admin-names").innerHTML = namesElement;
		document.getElementById("admin-names-label").innerText = key[0].toUpperCase() + key.slice(1);
	}
}

// generic update filter state for year & sex
function updateFilterState(event) {
	FilterState[event.srcElement.id] = event.target.value;
	console.log(FilterState);
}

// update admin-level state
function updateAdminLevelState(event) {
	if (FilterState["admin-level"] === event.target.value) { 
		FilterState["admin-level"] = "";
		FilterState["granularity"] = "";
		document.getElementById("grain").getElementsByTagName("option")[3].disabled = false;
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
			if (event.target.value != "") {
				document.getElementById("grain").value = "";
				FilterState["granularity"] = event.target.value;
				zvakavanda(event.target.value,adminNamesResponseHandler);
				document.getElementById("grain").removeAttribute("disabled")
				if (event.target.value === "district") { document.getElementById("grain").getElementsByTagName("option")[3].disabled = true; }
				else if (event.target.value === "province") { document.getElementById("grain").getElementsByTagName("option")[3].disabled = false; } 
			}
		}
	}
}

// update granularity state
function updateGrainState(event) {
	FilterState["granularity"] = event.target.value;
}

// Admin Level 
admin = document.getElementById("admin-level");
admin.addEventListener("change",updateAdminLevelState);

// Spatial Granularity
grain = document.getElementById("grain");
grain.addEventListener("change", updateGrainState);

// Year 
t = document.getElementById("year");
t.addEventListener("change", updateFilterState);

// Sex
sex = document.getElementById("sex");
sex.addEventListener("change", updateFilterState); 


// apply filters
dispatcher = document.getElementById("show-label");
dispatcher.addEventListener("click", () => {
											  if (validateFilters()) { diridza(FilterState); }
										   }
							);

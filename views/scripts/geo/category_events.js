// category state manager
var CategoryState = {
				     "categorySelected": "",
				     "filterActive": false,	
				    };

function updateCategoryState(event) {
	const frame = document.getElementById("filter-criteria");
	if (CategoryState["filterActive"]) {
		frame.style.visibility = "hidden";
		//document.getElementById("map").style.visibility = "visible";
		CategoryState["filterActive"] = false;
		CategoryState["categorySelected"] = "";
	}
	else {
		document.getElementById("map").style.visibility = "hidden";
		frame.style.visibility = "visible";
		CategoryState["filterActive"] = true;
		CategoryState["categorySelected"] = event.target.innerHTML;
	}
	console.log(CategoryState)
}

function createFilterHTML(category) {
	if (category === "Distribution") {
		return `
				<div id="admin-container">
					<label for="admin-level">Admin Level</label>
					<div>
					<select name="AdminLevels" id="admin-level">
						<option value=""></option>
						<option value="ward">Ward</option>
						<option value="district">District</option>
						<option value="province">Province</option>
					</select>
					</div>
				</div>
				<div id="grain-container">
					<label for="grain">Granularity</label>
					<div>
					<select name="grainValues" id="grain" disabled>
						<option value=""></option>
						<option value="ward">Ward</option>
						<option value="district">District</option>
						<option value="province">Province</option>
						</select>
					</div>
				</div>
				<div id="year-container">
					<label for="year">Year</label>
					<div>
					<select id="year" name="yearValues">
						<option value=""></option>
						<option value="2002">2002</option>
						<option value="2012">2012</option>
						<option value="2022">2022</option>
					</select>
					</div>
				</div>
				<div id="sex-container">
					<label for="sex">Sex</label>
					<div>
					<select id="sex" name="sexValues">
						<option value="total"></option>
						<option value="female">F</option>
						<option value="male">M</option>
					</select>
					</div>
				</div>`;
	}
}



function populateFilterContainer() {
	var container = document.getElementById("filter-container");
	const filterHTML = createFilterHTML("Distribution");
	container.innerHTML += filterHTML;
	console.log(container.innerHTML);
	var grain = document.getElementById("grain");
	grain.value = "district";
}

function insertAdminValuesFilter() {
	var filterContainer = document.getElementById("filter-container");
	filterContainer.innerHTML += `<div id="admin-names-container" >
									  <label for="admin-names">Province</label>
									  <div>
									  <select id="admin-names" name="adminNames" multiple>
									      <option value="Mashonaland Central">Masholanand Central</option>
									      <option value="Matebeleland South">Matebeleland South</option>
									      <option value="Uzumba Maramba Pfungwe">Uzumba Maramba Pfungwe</option>
									  </select>
									  </div>
								  </div>`;
}

const distro = document.getElementById("distribution");
distro.addEventListener("click",populateFilterContainer);
const household = document.getElementById("household");
household.addEventListener("click", insertAdminValuesFilter);






















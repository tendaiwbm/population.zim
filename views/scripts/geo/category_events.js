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

const distro = document.getElementById("distribution");
distro.addEventListener("click", updateCategoryState);



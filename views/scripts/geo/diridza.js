var BASE = "http://population.zim:8081/";
var API_GEO_STUB = "api/geo";

function munyayi(mahobho,responseHandler) {
	var mutumwa = new XMLHttpRequest();
	mutumwa.onreadystatechange = function(event) {
												 	if (mutumwa.readyState === 4 && mutumwa.status === 200) {
												 		responseHandler(event,mutumwa.response);
												 	}
												 }
	mutumwa.open("GET",mahobho,true);
	mutumwa.send();
}

// penengura mhinduro, gadzirisa map
function mhinduro(event,mutumwa) {
	console.log(event);
	const map = document.getElementById("map");
	CategoryState["filterActive"] = false;
	document.getElementById("map").style.visibility = "visible";
	geometryResponseHandler(JSON.parse(mutumwa));
	//map.innerText = JSON.stringify(JSON.parse(mutumwa),undefined,2);
}


// tumira, penengura mhinduro, gadzirisa map
function diridza(params) {
	var mahobho = `${BASE}${API_GEO_STUB}?category=${CategoryState["categorySelected"].toLowerCase()}&admin=${params["admin-level"]}&grain=${params["granularity"]}&year=${params["year"]}&sex=male`;
	munyayi(mahobho,params["zvadzoka"]);
	return;
}

function zvakavanda(level,responseHandler) {
	var mahobho = `${BASE}${API_GEO_STUB}/zvakavanda?admin=${level}`;
	console.log("Meta URL  >>  " + mahobho);
	munyayi(mahobho,responseHandler);
}


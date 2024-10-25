(function displayFilterWindow(event) {
	var projectName = "populationZim";
	console.log("Starting: " + projectName + " --> geo.");
})();

var map = L.map('map', {
						 crs: L.CRS.EPSG4326,
						 layers: [],
						 center: [-17.817452,31.052431],
						 zoom: 12,	
						}
				);

map.attributionControl.setPrefix("");


function colour(feature) {
	return feature > 3500 ? "#a8281eff" : 
		   feature > 2500 ? "#d83020ff" :
		   feature > 1500 ? "#f07062ff" :
		   					"#f89b91ff" ;
};	

function geometryResponseHandler(response) {
	for (i=0;i<response["coordinates"].length;i++) {
		L.polygon(response["coordinates"][i],{
											  color: "black",
											  weight: 1.2,
											  fillColor: colour(response["values"][i]), 
											  fillOpacity: 1,
											  attributes: {
											  				"pop": response["values"][i]
											  			  }
								             }
		).addTo(map);
	}
	map.attributionControl.addAttribution("ZIMSTAT  |  Leaflet  |  HDX  |  ESRI")
	map.zoomControl.setPosition("topright");
	document.getElementById("filter-container").style.opacity = "60%";
}

/*
/// Esri color ramps - Esri Red 1
// #a8281eff,#d83020ff,#f07062ff,#f89b91ff,#fbb1a8ff
const colors = ["#a8281eff", "#d83020ff", "#f07062ff", "#f89b91ff", "#fbb1a8ff"];
*/
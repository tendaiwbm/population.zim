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
	return feature > 3500 ? "#4d0000" : 
		   feature > 2500 ? "#4d0000" :
		   feature > 1500 ? "#cca300" :
		   					"#f2f2f2";
};	

function geometryResponseHandler(response) {
	for (i=0;i<response["coordinates"].length;i++) {
		L.polygon(response["coordinates"][i],{
											  color: "#d9d9d9",
											  weight: 1.2,
											  fillColor: colour(response["values"][i]), 
											  fillOpacity: 1,
											  attributes: {
											  				"pop": response["values"][i]
											  			  }
								             }
		).addTo(map);
	}
	map.attributionControl.addAttribution("ZIMSTAT  |  Leaflet  |  HDX")
	map.zoomControl.setPosition("topright");
}

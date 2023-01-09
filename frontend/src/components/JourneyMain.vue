<template>
	<div class="container-fluid p-3">
		<div class="row">
			<div class="col-8 min-vh-80 d-flex flex-column">
				<div class="row flex-grow-1">
					<div class="col-md-12">
						<div id="map"></div>
					</div>
				</div>
			</div>
			<div class="col-4">
				<div class="row">
					<div class="col-md-12">
						<h3>Chosen places</h3>
					</div>
				</div>
				<div class="row">
					<div class="col-md-12 min-vh-80 d-flex flex-column border rounded">
						<div class="row">
							<div>No places chosen yet...</div>
						</div>
						<div class="row mt-auto">
							<button class="btn btn-primary" @click="this.$store.commit('setIsLoading', true)">Generate journey</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import "leaflet/dist/leaflet.css";
var L = require('leaflet');
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});
import 'leaflet-geosearch/dist/geosearch.css';
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch'

export default {
	name: 'JourneyMain',
    mounted(){
		let map = L.map('map', {
			scrollWheelZoom: true
		});
		this.map = map
		map.setView([52.232, 21.028], 12);
		L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
		}).addTo(map);
		const search = new GeoSearchControl({
			provider: new OpenStreetMapProvider(),
			style: 'bar',
		});

		map.addControl(search);
    },
}
</script>

<style>
#map{
	width: 100%;
	height: 100%;
}
.min-vh-80{
	min-height: 80vh;
}
</style>

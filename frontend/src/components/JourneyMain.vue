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

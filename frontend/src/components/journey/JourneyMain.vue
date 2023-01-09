<template>
	<div class="container-fluid p-3">
		<div class="row">
			<div class="col-6 min-vh-80 d-flex flex-column">
				<div class="row flex-grow-1">
					<div class="col-md-12">
						<div id="map"></div>
					</div>
				</div>
			</div>
			<div class="col-6">
				<div class="row">
					<div class="col-md-12">
						<h3>Chosen places</h3>
					</div>
				</div>
				<div class="row">
					<div class="col-md-12 min-vh-80 d-flex flex-column border rounded">
						<div class="row">
							<div class="col-12">
								<table class="table table-hover" v-if="chosenPlaces.length > 0">
								<thead>
									<tr>
										<th scope="col">Address</th>
										<th scope="col">Openning hours</th>
										<th scope="col">Visiting time</th>
										<th scope="col"></th>
									</tr>
								</thead>
								<tbody>
									<tr v-for="place of chosenPlaces" :key="place">
										<JourneyRecord @placeAccepted="onPlaceAccepted" @placeRemoved="onPlaceRemoved" :place="place" />
									</tr>
								</tbody>
								</table>
								<div v-else>
									No places chosen yet...
								</div>
							</div>
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
import JourneyRecord from './JourneyRecord.vue'
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
	components: {
		JourneyRecord,
	},
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
		map.on('geosearch/showlocation', (event) => {
			this.chosenPlaces.push({
				identifier: this.placesCounter,
				address: event.marker.getPopup().getContent(),
				lat: event.location.y,
				lng: event.location.x,
			});
			console.log(this.chosenPlaces)
			this.placesCounter++;
		});
    },
	data() {
		return {
			chosenPlaces: [],
			placesCounter: 1,
		}
	},
	methods: {
		onPlaceAccepted(placeIdentifier) {
			console.log("accepted", placeIdentifier)
		},
		onPlaceRemoved(placeIdentifier) {
			this.chosenPlaces = this.chosenPlaces.filter(function( obj ) {
				return obj.identifier !== placeIdentifier;
			});
		}
	}
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

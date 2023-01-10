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
								<table class="table" v-if="chosenPlaces.length > 0">
								<thead>
									<tr>
										<th scope="col">Address</th>
										<th scope="col">Openning hours</th>
										<th scope="col">Visiting time</th>
										<th scope="col"></th>
									</tr>
								</thead>
								<tbody>
									<JourneyRecord v-for="place of chosenPlaces" :key="place" :place="place"
													@placeAccepted="onPlaceAccepted" @placeRemoved="onPlaceRemoved"/>
								</tbody>
								</table>
								<div v-else>
									No places chosen yet...
								</div>
							</div>
						</div>
						<div class="row mt-auto">
							<button class="btn btn-primary" @click="calculateJourney">Generate journey</button>
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
		this.map = L.map('map', {scrollWheelZoom: true});
		this.map.setView([52.232, 21.028], 12);
		L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
		}).addTo(this.map);
		const search = new GeoSearchControl({
			provider: new OpenStreetMapProvider(),
			style: 'bar',
			showMarker: false,
			autoClose: true,
			keepResult: false,
		});
		this.map.addControl(search);
		this.map.on('geosearch/showlocation', (event) => {
			for (const place of this.chosenPlaces) {
				if (!place.accepted) 
					this.map.removeLayer(place.marker);
			}
			this.chosenPlaces = this.chosenPlaces.filter(function( obj ) {
				return obj.accepted;
			});
			let randomColor = '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0');
			let marker = new L.Marker([event.location.y, event.location.x], {
				icon: this.setupIcon(randomColor)
			});
			marker.bindPopup(event.location.label);
			let identifier = this.placesCounter;
			this.chosenPlaces.push({
				identifier: identifier,
				address: event.location.label,
				lat: event.location.y,
				lng: event.location.x,
				marker: marker,
				accepted: false,
				color: randomColor,
			});
			const index = this.chosenPlaces.map(e => e.identifier).indexOf(identifier);
			this.chosenPlaces.at(index).marker.addTo(this.map);
			marker.on("mouseover", () => {
				this.chosenPlaces.at(index).highlighted = true
				marker.openPopup();
			})
			marker.on("mouseout", () => {
				this.chosenPlaces.at(index).highlighted = false
				marker.closePopup();
			})
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
		setupIcon(color) {
			const markerHtmlStyles = `
				background-color: ${color};
				width: 2rem;
				height: 2rem;
				display: block;
				left: -1rem;
				top: -1rem;
				position: relative;
				border-radius: 3rem 3rem 0;
				transform: rotate(45deg);
				border: 1px solid #FFFFFF`
			return L.divIcon({
				className: "custom-pin",
				iconAnchor: [0, 24],
				labelAnchor: [-6, 0],
				popupAnchor: [0, -36],
				html: `<span style="${markerHtmlStyles}" />`
			})
		},
		onPlaceAccepted(placeIdentifier) {
			const index = this.chosenPlaces.map(e => e.identifier).indexOf(placeIdentifier);
			this.chosenPlaces[index].accepted = true;
		},
		onPlaceRemoved(placeIdentifier) {
			const index = this.chosenPlaces.map(e => e.identifier).indexOf(placeIdentifier);
			this.map.removeLayer(this.chosenPlaces[index].marker);
			this.chosenPlaces = this.chosenPlaces.filter(function( obj ) {
				return obj.identifier !== placeIdentifier;
			});
		},
		calculateJourney() {
			this.$store.commit('setIsLoading', true)
		}
	}
}
</script>

<style scoped>
#map{
	width: 100%;
	height: 100%;
}
.min-vh-80{
	min-height: 80vh;
}
</style>

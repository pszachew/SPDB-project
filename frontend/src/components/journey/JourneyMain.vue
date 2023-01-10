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
import axios from 'axios';
import "leaflet/dist/leaflet.css";
var L = require('leaflet');
import 'leaflet-geosearch/dist/geosearch.css';
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch'

import JourneyRecord from './JourneyRecord.vue'

import CustomMarker from '../../helpers/CustomMarker.js'
import JourneyPlace from '../../helpers/JourneyPlace.js'

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
			let marker = new CustomMarker(event.location.y, event.location.x, event.location.label);
			let identifier = this.placesCounter;
			this.chosenPlaces.push(new JourneyPlace(identifier, event.location.label,
													event.location.y, event.location.x,
													marker.marker, false, marker.color));
			const index = this.chosenPlaces.map(e => e.identifier).indexOf(identifier);
			this.chosenPlaces.at(index).marker.addTo(this.map);
			marker.marker.on("mouseover", () => {
				this.chosenPlaces.at(index).highlighted = true
				marker.marker.openPopup();
			})
			marker.marker.on("mouseout", () => {
				this.chosenPlaces.at(index).highlighted = false
				marker.marker.closePopup();
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
			let placesData = []
			this.chosenPlaces.forEach(place => {
				if (place.accepted) {
					placesData.push(place.getExportData())
				}
			})
			axios.post(`/calculate-journey`, {
				data: placesData
			}).then(response => {
				console.log(response)
			}).catch(e => {
				console.error(e)
			}).finally(() => {
				this.$store.commit('setIsLoading', false)
			})
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

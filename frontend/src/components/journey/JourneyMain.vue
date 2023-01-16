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
										<!-- <th scope="col">Openning hours</th>
										<th scope="col">Visiting time</th> -->
										<th scope="col"></th>
									</tr>
								</thead>
								<tbody>
									<JourneyRecord v-for="place of chosenPlaces" :key="place" :place="place" :calculated="calculated"
													@placeAccepted="onPlaceAccepted" @placeRemoved="onPlaceRemoved"
													@visitingTimeChanged="OnVisitingTimeChanged" @openingHoursChanged="OnOpeningHoursChanged" />
								</tbody>
								</table>
								<div v-else>
									No places chosen yet...
								</div>
							</div>
						</div>
						<div class="row mt-auto" v-if="!calculated">
							<div class="col-12">
								<div class="row">
									<div class="col-4">Transportation methods</div>
									<!-- <div class="col-4">Starting time</div>
									<div class="col-4">Ending time</div> -->
								</div>
								<div class="row">
									<div class="col-4">
										<div class="row">
											<button @click="handleTransportation('car')" class="btn mx-1 col-3"
													:class="{'btn-outline-info': !transportationTypes.car, 'btn-info': transportationTypes.car}">
												<font-awesome-icon icon="fa-solid fa-car" size="1x"/>
											</button>
											<button @click="handleTransportation('bike')" class="btn mx-1 col-3" disabled
													:class="{'btn-outline-info': !transportationTypes.bike, 'btn-info': transportationTypes.bike}">
												<font-awesome-icon icon="fa-solid fa-person-biking" size="1x"/>
											</button>
											<button @click="handleTransportation('foot')" class="btn mx-1 col-3" disabled
													:class="{'btn-outline-info': !transportationTypes.foot, 'btn-info': transportationTypes.foot}">
												<font-awesome-icon icon="fa-solid fa-person-walking" size="1x"/>
											</button>
										</div>
									</div>
									<div class="col-4">
										<!-- <Datepicker v-model="startingTime" time-picker /> -->
									</div>
									<div class="col-4">
										<!-- <Datepicker v-model="endingTime" time-picker /> -->
									</div>
								</div>
							</div>
							<button class="btn btn-primary mt-1" @click="calculateJourney">Generate journey</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import 'leaflet-geosearch/dist/geosearch.css';
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faCar, faPersonBiking, faPersonWalking } from '@fortawesome/free-solid-svg-icons'
library.add(faCar)
library.add(faPersonBiking)
library.add(faPersonWalking)

import '@vuepic/vue-datepicker/dist/main.css';
import Datepicker from '@vuepic/vue-datepicker';

import JourneyRecord from './JourneyRecord.vue'

import CustomMarker from '../../helpers/CustomMarker.js'
import JourneyPlace from '../../helpers/JourneyPlace.js'

export default {
	name: 'JourneyMain',
	components: {
		JourneyRecord,
		// eslint-disable-next-line
        Datepicker,
	},
    setup() {
        return {
            startingTime: ref({hours: 8, minutes: 0}),
            endingTime: ref(),
        }
    },
    mounted(){
		this.map = L.map('map', {scrollWheelZoom: true});
		this.map.setView([52.232, 21.028], 12);
		this.map.on("click", (event) => {
			if (this.calculated){
				return
			}
			if (!this.startingPointMarker){
				this.startingPointMarker = new CustomMarker(event.latlng.lat, event.latlng.lng, 'Starting point');
				this.startingPointMarker.marker.on("mouseover", () => this.startingPointMarker.marker.openPopup())
				this.startingPointMarker.marker.on("mouseout", () => this.startingPointMarker.marker.closePopup())
				this.startingPointMarker.marker.addTo(this.map);
			} else {
				this.startingPointMarker.marker.setLatLng(event.latlng);
			}
		})
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
			if (this.calculated){
				return
			}
			for (const place of this.chosenPlaces) {
				if (!place.accepted) 
					this.map.removeLayer(place.marker.marker);
			}
			this.chosenPlaces = this.chosenPlaces.filter(obj => obj.accepted);
			let marker = new CustomMarker(event.location.y, event.location.x, event.location.label);
			let identifier = this.placesCounter;
			this.chosenPlaces.push(new JourneyPlace(identifier, event.location.label,
													event.location.y, event.location.x,
													marker, false, marker.color));
			const index = this.chosenPlaces.findIndex(e => e.id === identifier);
			this.chosenPlaces.at(index).marker.marker.addTo(this.map);
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
			transportationTypes: {
				car: true,
				bike: false,
				foot: false,
				// public: false,
			},
			startingPointMarker: null,
			calculated: false,
		}
	},
	methods: {
		onPlaceAccepted(placeId) {
			const index = this.chosenPlaces.map(e => e.id).indexOf(placeId);
			this.chosenPlaces[index].accepted = true;
		},
		onPlaceRemoved(placeId) {
			const index = this.chosenPlaces.map(e => e.id).indexOf(placeId);
			this.map.removeLayer(this.chosenPlaces[index].marker.marker);
			this.chosenPlaces = this.chosenPlaces.filter(function( obj ) {
				return obj.id !== placeId;
			});
		},
		OnVisitingTimeChanged(placeId, date) {
			const index = this.chosenPlaces.map(e => e.id).indexOf(placeId);
			this.chosenPlaces[index].visitingTime = date;
		},
		OnOpeningHoursChanged(placeId, date) {
			const index = this.chosenPlaces.map(e => e.id).indexOf(placeId);
			this.chosenPlaces[index].openingTime = date[0];
			this.chosenPlaces[index].closingTime = date[1];
		},
		handleTransportation(transportationType) {
			this.transportationTypes[transportationType] = !this.transportationTypes[transportationType];
		},
		validateData() {
			if (!this.startingPointMarker) {
				this.$toast.error(`You have to choose starting point by clicking on the map!`);
				return false
			}
			if (!this.chosenPlaces.length) {
				this.$toast.error(`You have to choose at least one place!`);
				return false
			}
			if (Object.values(this.transportationTypes).every(item => item === false)) {
				this.$toast.error(`You have to choose at least one transportation type!`);
				return false
			}
			if (this.chosenPlaces.filter(obj => obj.accepted).length === 0) {
				this.$toast.error(`You have to choose at least one place!`);
				return false
			}
			return true
		},
		calculateJourney() {
			if (!this.validateData()) {
				return
			}
			this.$store.commit('setIsLoading', true)
			let placesData = []
			this.chosenPlaces = this.chosenPlaces.filter(place => {
				if (place.accepted) {
					placesData.push(place.getExportData())
				}
				return place.accepted
			})
			let msg = {
				"places": placesData,
				"transportationTypes": this.transportationTypes,
				"startingTime": this.startingTime,
				"endingTime": this.endingTime,
				"startingPoint": this.startingPointMarker.marker.getLatLng(),
			}
			axios.post(`/calculate-journey`, msg).then(response => {
				let paths = Object.values(response.data.path);
				let order = response.data.order.slice(1, response.data.order.length);
				this.drawRoute(paths[0], this.startingPointMarker.color);
				this.startingPointMarker.changeText(1);
				paths.slice(1, paths.length).forEach((path, i) => {
					this.chosenPlaces.at(order[i]).marker.changeText(i + 2);
					this.drawRoute(path, this.chosenPlaces.at(order[i]).color);
				})
				this.chosenPlaces.at(order.at(-1)).marker.changeText(order.length + 1);
				this.calculated = true;
			}).catch(e => {
				console.error(e)
			}).finally(() => {
				this.$store.commit('setIsLoading', false)
			})
		},
		drawRoute(path, color) {
			let routeData = path.map(point => {
				let pointData = JSON.parse(point[0]).coordinates;
				return [pointData[0], pointData[1]]
			})
			let data = {
				"type": "MultiLineString",
				"coordinates": [routeData],
			}
			let mapRoute = new L.GeoJSON(data, {
				style: function () {
					return {color: color};
				},
			});
			mapRoute.addTo(this.map);
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

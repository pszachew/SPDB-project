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
													@placeAccepted="onPlaceAccepted" @placeRemoved="onPlaceRemoved"
													@visitingTimeChanged="OnVisitingTimeChanged" @openingHoursChanged="OnOpeningHoursChanged" />
								</tbody>
								</table>
								<div v-else>
									No places chosen yet...
								</div>
							</div>
						</div>
						<div class="row mt-auto">
							<div class="col-12">
								<div class="row">
									<div class="col-4">Transportation methods</div>
									<div class="col-4">Starting time</div>
									<div class="col-4">Ending time</div>
								</div>
								<div class="row">
									<div class="col-4">
										<div class="row">
											<button @click="handleTransportation('car')" class="btn mx-1 col-3" 
													:class="{'btn-outline-info': !transportationTypes.car, 'btn-info': transportationTypes.car}">
												<font-awesome-icon icon="fa-solid fa-car" size="1x"/>
											</button>
											<button @click="handleTransportation('bike')" class="btn mx-1 col-3"
													:class="{'btn-outline-info': !transportationTypes.bike, 'btn-info': transportationTypes.bike}">
												<font-awesome-icon icon="fa-solid fa-person-biking" size="1x"/>
											</button>
											<button @click="handleTransportation('foot')" class="btn mx-1 col-3"
													:class="{'btn-outline-info': !transportationTypes.foot, 'btn-info': transportationTypes.foot}">
												<font-awesome-icon icon="fa-solid fa-person-walking" size="1x"/>
											</button>
										</div>
									</div>
									<div class="col-4">
										<Datepicker v-model="startingTime" />
									</div>
									<div class="col-4">
										<Datepicker v-model="endingTime" />
									</div>
								</div>
							</div>
							<div class="m-1 px-0">
							</div>
							<button class="btn btn-primary" @click="calculateJourney">Generate journey</button>
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
var L = require('leaflet');
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
        Datepicker
	},
    setup() {
        return {
            startingTime: ref(new Date()),
            endingTime: ref(),
        }
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
			transportationTypes: {
				car: false,
				bike: false,
				foot: false,
				// public: false,
			},
			startingPoint: {
				lat: 52.232,
				lng: 21.028,
			}
		}
	},
	methods: {
		onPlaceAccepted(placeId) {
			const index = this.chosenPlaces.map(e => e.id).indexOf(placeId);
			this.chosenPlaces[index].accepted = true;
		},
		onPlaceRemoved(placeId) {
			const index = this.chosenPlaces.map(e => e.id).indexOf(placeId);
			this.map.removeLayer(this.chosenPlaces[index].marker);
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
		calculateJourney() {
			this.$store.commit('setIsLoading', true)
			let placesData = []
			this.chosenPlaces.forEach(place => {
				if (place.accepted) {
					placesData.push(place.getExportData())
				}
			})
			let msg = {
				"places": placesData,
				"transportation_types": this.transportationTypes,
				"starting_time": this.startingTime,
				"ending_time": this.endingTime,
				"startingPoint": this.startingPoint
			}
			axios.post(`/calculate-journey`, {
				data: msg
			}).then(response => {
				console.log(response)
			}).catch(e => {
				console.error(e)
			}).finally(() => {
				this.$store.commit('setIsLoading', false)
			})
		},
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

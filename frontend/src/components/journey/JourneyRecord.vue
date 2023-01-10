<template>
    <tr ref="row" class="row-border" :class="{highlighted: place.highlighted}">
        <td>{{ place.address }}</td>
        <td><Datepicker v-model="openningHours" range time-picker /></td>
        <td><Datepicker v-model="visitingTime" time-picker /></td>
        <td>
            <div class="no-break" v-if="!accepted">
                <button class="btn btn-outline-success mx-1" @click="acceptPlace()">
                    <font-awesome-icon icon="fa-solid fa-check"/>
                </button>
                <button class="btn btn-outline-danger mx-1" @click="removePlace()">
                    <font-awesome-icon icon="fa-solid fa-x"/>
                </button>
            </div>
            <div v-else>
                <button class="btn btn-danger mx-1" @click="removePlace()">
                    <font-awesome-icon icon="fa-solid fa-trash-can"/>
                </button>
            </div>
        </td>
    </tr>
</template>
<script>
import { ref } from 'vue';
import '@vuepic/vue-datepicker/dist/main.css';
import Datepicker from '@vuepic/vue-datepicker';

import { library } from '@fortawesome/fontawesome-svg-core'
import { faCheck, faX, faTrashCan } from '@fortawesome/free-solid-svg-icons'
library.add(faCheck)
library.add(faX)
library.add(faTrashCan)

export default {
	name: 'JourneyMain',
    components: {
        Datepicker
    },
    props: [
        "place",
    ],
    emits: ["placeAccepted", "placeRemoved"],
    setup() {
        const openningHours = ref([
            {hours: 8, minutes: 0},
            {hours: 20, minutes: 0}
        ])
        const visitingTime = ref({hours: 0, minutes: 0})

        return {
            openningHours,
            visitingTime
        }
    },
    methods: {
        acceptPlace() {
            this.accepted = true
            this.$emit("placeAccepted", this.place.identifier)
        },
        removePlace() {
            this.accepted = false
            this.$emit("placeRemoved", this.place.identifier)
        },
    },
    data() {
        return {
            accepted: false
        }
    },
}
</script>

<style scoped>
.no-break{
    white-space: nowrap
}
.row-border{
    border-bottom: 2px solid v-bind('place.color')
}
.highlighted {
    background-color: v-bind('place.color')
}
</style>

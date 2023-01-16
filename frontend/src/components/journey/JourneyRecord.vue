<template>
    <tr class="row-border" :class="{highlighted: place.highlighted}">
        <td>{{ place.address }}</td>
        <td><Datepicker v-model="openningHours" range time-picker :disabled="calculated" /></td>
        <td><Datepicker v-model="visitingTime" time-picker :disabled="calculated" /></td>
        <td>
            <div v-if="!calculated">
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
        "calculated"
    ],
    emits: ["placeAccepted", "placeRemoved", "openingHoursChanged", "visitingTimeChanged"],
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
    mounted() {
        this.$emit("openingHoursChanged", this.place.id, this.openningHours)
        this.$emit("visitingTimeChanged", this.place.id, this.visitingTime)
    },
    watch: {
        openningHours() {
            this.$emit("openingHoursChanged", this.place.id, this.openningHours)
        },
        visitingTime() {
            this.$emit("visitingTimeChanged", this.place.id, this.visitingTime)
        }
    },
    methods: {
        acceptPlace() {
            this.accepted = true
            this.$emit("placeAccepted", this.place.id)
        },
        removePlace() {
            this.accepted = false
            this.$emit("placeRemoved", this.place.id)
        }
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

export default class JourneyPlace {
    constructor(id, address, lat, lng, marker, accepted, color) {
        this.id = id;
        this.address = address;
        this.lat = lat;
        this.lng = lng;
        this.marker = marker;
        this.accepted = accepted;
        this.color = color;
        this.openingTime = null;
        this.closingTime = null;
        this.visitingTime = null;
    }

    getExportData() {
        return {
            lat: this.lat,
            lng: this.lng,
            openingTime: this.openingTime,
            closingTime: this.closingTime,
            visitingTime: this.visitingTime,
            address: this.address,
        }
    }
}

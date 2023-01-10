var L = require('leaflet');

export default class CustomMarker {
    constructor(lat, lng, label) {
        this.color = this.getRandomColor();
        this.marker = new L.Marker([lat, lng], {
            icon: this.setupStyle(this.color)
        });
        this.marker.bindPopup(label);
    }

    getRandomColor() {
        return '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0');
    }

    setupStyle(color) {
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
    }
}

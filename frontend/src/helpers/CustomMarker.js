var L = require('leaflet');

export default class CustomMarker {
    constructor(lat, lng, label) {
        this.uuid = "S" + Math.random().toString(16).slice(2);
        this.color = this.getRandomColor();
        this.marker = new L.Marker([lat, lng], {
            icon: this.setupStyle(this.color)
        });
        this.marker.bindPopup(label);
    }

    getRandomColor() {
        return '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0');
    }

    changeText(text) {
        document.querySelector(`#${this.uuid} > p`).textContent = text;
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
        const textStyle = `
            position: relative;
            left: -0.4rem;
            top: -2.5rem;
            text-align: center;
        `
        return L.divIcon({
            className: "custom-pin",
            iconAnchor: [0, 24],
            labelAnchor: [-6, 0],
            popupAnchor: [0, -36],
            html: `<div id="${this.uuid}"><span style="${markerHtmlStyles}"></span><p style="${textStyle}"></p></div>`
        })
    }
}

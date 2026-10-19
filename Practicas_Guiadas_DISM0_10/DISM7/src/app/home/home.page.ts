import { Component } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/angular';
import * as Leaflet from 'leaflet';
import { icon, Marker } from 'leaflet';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonHeader, IonToolbar, IonTitle, IonContent],
})
export class HomePage {
  map?: Leaflet.Map;
  constructor() {}
  ionViewDidEnter() {
    this.leafletMap();
  }
  leafletMap() {
    const iconRetinaUrl = 'assets/marker-icon-2x.png';
    const iconUrl = 'assets/marker-icon.png';
    const shadowUrl = 'assets/marker-shadow.png';
    const iconDefault = icon({
      iconRetinaUrl,
      iconUrl,
      shadowUrl,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      tooltipAnchor: [16, -28],
      shadowSize: [41, 41],
    });
    Marker.prototype.options.icon = iconDefault;
    this.map = Leaflet.map('mapId').setView([38.38735, -0.51238], 4);
    Leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'DISM © Ionic Leaflet',
    }).addTo(this.map);
    Leaflet.marker([38.38735, -0.51238]).addTo(this.map).bindPopup('Alicante').openPopup();
    Leaflet.marker([41.38113, 2.12244]).addTo(this.map).bindPopup('Barcelona').openPopup();
  }
}

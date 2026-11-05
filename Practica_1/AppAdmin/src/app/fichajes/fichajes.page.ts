import { Component, OnInit } from '@angular/core';
import { ApiService, Fichaje, Usuario } from '../services/api';
import * as Leaflet from 'leaflet';

@Component({
  selector: 'app-fichajes',
  templateUrl: './fichajes.page.html',
  styleUrls: ['./fichajes.page.scss'],
  standalone: false
})
export class FichajesPage implements OnInit {
  fichajes: Fichaje[] = [];
  usuarios: Usuario[] = [];
  fichajesFiltrados: Fichaje[] = [];

  filtroTexto = '';
  filtroUsuario: number | null = null;
  filtroFechaInicio = '';
  filtroFechaFin = '';

  fichajeModalMapa: Fichaje | null = null;
  mostrarModalMapa = false;
  mapaLeaflet?: Leaflet.Map;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.api.getUsuarios().subscribe(u => this.usuarios = u);
    this.aplicarFiltros();
  }

  aplicarFiltros() {
    const filtros: any = {};
    if (this.filtroUsuario) filtros.idUsuario = this.filtroUsuario;
    if (this.filtroFechaInicio) filtros.fechaInicio = this.filtroFechaInicio;
    if (this.filtroFechaFin) filtros.fechaFin = this.filtroFechaFin;

    this.api.getFichajes(filtros).subscribe(data => {
      this.fichajes = data;
      this.filtrarPorTexto();
    });
  }

  filtrarPorTexto() {
    if (!this.filtroTexto || this.filtroTexto.trim() === '') {
      this.fichajesFiltrados = [...this.fichajes];
      return;
    }
    const q = this.filtroTexto.toLowerCase();
    this.fichajesFiltrados = this.fichajes.filter(f =>
      (f.NombreUsuario && f.NombreUsuario.toLowerCase().includes(q)) ||
      (f.NombreTrabajo && f.NombreTrabajo.toLowerCase().includes(q)) ||
      (f.FechaHoraEntrada && f.FechaHoraEntrada.includes(q))
    );
  }

  limpiarFiltros() {
    this.filtroTexto = '';
    this.filtroUsuario = null;
    this.filtroFechaInicio = '';
    this.filtroFechaFin = '';
    this.aplicarFiltros();
  }

  abrirMapa(f: Fichaje) {
    this.fichajeModalMapa = f;
    this.mostrarModalMapa = true;
    setTimeout(() => {
      this.inicializarMapa(f.GeolocalizacionLatitud, f.GeolocalizacionLongitud, f.NombreUsuario || 'Empleado', f.FechaHoraEntrada);
    }, 400);
  }

  cerrarModalMapa() {
    if (this.mapaLeaflet) {
      this.mapaLeaflet.remove();
      this.mapaLeaflet = undefined;
    }
    this.mostrarModalMapa = false;
    this.fichajeModalMapa = null;
  }

  inicializarMapa(lat: number, lon: number, usuario: string, fecha: string) {
    const iconRetinaUrl = 'assets/marker-icon-2x.png';
    const iconUrl = 'assets/marker-icon.png';
    const shadowUrl = 'assets/marker-shadow.png';
    const iconDefault = Leaflet.icon({
      iconRetinaUrl,
      iconUrl,
      shadowUrl,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
    Leaflet.Marker.prototype.options.icon = iconDefault;

    const mapContainer = document.getElementById('mapAdminId');
    if (!mapContainer) return;

    this.mapaLeaflet = Leaflet.map('mapAdminId').setView([lat, lon], 15);
    Leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'DISM Fichajes © OpenStreetMap'
    }).addTo(this.mapaLeaflet);

    Leaflet.marker([lat, lon])
      .addTo(this.mapaLeaflet)
      .bindPopup(`<b>${usuario}</b><br>Fichaje: ${fecha}<br>Coord: ${lat.toFixed(5)}, ${lon.toFixed(5)}`)
      .openPopup();
  }
}

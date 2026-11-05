import { Component, OnInit } from '@angular/core';
import { ApiService, Fichaje, Usuario } from '../services/api';
import { Router } from '@angular/router';
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

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  ngOnInit() {
    this.cargarDatos();
  }

  ionViewWillEnter() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.api.getUsuarios().subscribe(u => this.usuarios = u || []);
    this.aplicarFiltros();
  }

  aplicarFiltros() {
    const filtros: any = {};
    if (this.filtroUsuario) filtros.idUsuario = this.filtroUsuario;
    if (this.filtroFechaInicio) filtros.fechaInicio = this.filtroFechaInicio;
    if (this.filtroFechaFin) filtros.fechaFin = this.filtroFechaFin;

    this.api.getFichajes(filtros).subscribe({
      next: (data) => {
        this.fichajes = data || [];
        this.filtrarPorTexto();
      },
      error: () => {
        this.fichajes = [];
        this.fichajesFiltrados = [];
      }
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

  abrirMapa(fichaje: Fichaje) {
    this.fichajeModalMapa = fichaje;
    this.mostrarModalMapa = true;
    setTimeout(() => {
      this.iniciarMapaLeaflet(fichaje.GeolocalizacionLatitud, fichaje.GeolocalizacionLongitud);
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

  iniciarMapaLeaflet(lat: number, lon: number) {
    const contenedor = document.getElementById('mapAdminId');
    if (!contenedor) return;

    if (this.mapaLeaflet) {
      this.mapaLeaflet.remove();
    }

    this.mapaLeaflet = Leaflet.map('mapAdminId').setView([lat, lon], 16);

    Leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(this.mapaLeaflet);

    const iconoFichaje = Leaflet.icon({
      iconUrl: 'assets/marker-icon.png',
      shadowUrl: 'assets/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34]
    });

    Leaflet.marker([lat, lon], { icon: iconoFichaje })
      .addTo(this.mapaLeaflet)
      .bindPopup(`<b>${this.fichajeModalMapa?.NombreUsuario || 'Fichaje'}</b><br>${this.fichajeModalMapa?.FechaHoraEntrada}`)
      .openPopup();
  }

  logout() {
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}

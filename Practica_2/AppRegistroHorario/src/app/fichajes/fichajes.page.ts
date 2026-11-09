import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService, Fichaje, Usuario } from '../services/api';
import { AlertController, ToastController } from '@ionic/angular';
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
    private alertCtrl: AlertController,
    private toastCtrl: ToastController,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.cargarDatos();
  }

  ionViewWillEnter() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.api.getUsuarios().subscribe(u => {
      this.usuarios = u || [];
      this.cdr.detectChanges();
    });
    this.aplicarFiltros();
  }

  aplicarFiltros() {
    const filtros: any = {};
    if (this.filtroUsuario) filtros.idUsuario = this.filtroUsuario;
    if (this.filtroFechaInicio) filtros.fechaInicio = this.filtroFechaInicio;
    if (this.filtroFechaFin) filtros.fechaFin = this.filtroFechaFin;

    this.api.getFichajes(filtros).subscribe({
      next: (data) => {
        this.fichajes = [...(data || [])];
        this.fichajesFiltrados = [...this.fichajes];
        this.cdr.detectChanges();
      },
      error: () => {
        this.fichajes = [];
        this.fichajesFiltrados = [];
        this.cdr.detectChanges();
      }
    });
  }

  limpiarFiltros() {
    this.filtroTexto = '';
    this.filtroUsuario = null;
    this.filtroFechaInicio = '';
    this.filtroFechaFin = '';
    this.aplicarFiltros();
  }

  async confirmarEliminar(idFichaje: number) {
    const alert = await this.alertCtrl.create({
      header: 'Confirmar Eliminación',
      message: '¿Estás seguro de que deseas eliminar este registro de fichaje?',
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        {
          text: 'Eliminar',
          role: 'destructive',
          handler: () => {
            this.api.eliminarFichaje(idFichaje).subscribe({
              next: async () => {
                this.aplicarFiltros();
                const t = await this.toastCtrl.create({
                  message: 'Fichaje eliminado correctamente',
                  duration: 2500,
                  color: 'success'
                });
                await t.present();
              },
              error: async (err) => {
                const t = await this.toastCtrl.create({
                  message: err.error?.message || 'Error al eliminar fichaje',
                  duration: 3000,
                  color: 'danger'
                });
                await t.present();
              }
            });
          }
        }
      ]
    });
    await alert.present();
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

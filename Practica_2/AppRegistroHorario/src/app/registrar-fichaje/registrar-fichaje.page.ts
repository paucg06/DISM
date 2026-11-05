import { Component, OnInit } from '@angular/core';
import { ApiService, Fichaje, Trabajo, Usuario } from '../services/api';
import { Geolocation } from '@capacitor/geolocation';
import { ToastController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registrar-fichaje',
  templateUrl: './registrar-fichaje.page.html',
  styleUrls: ['./registrar-fichaje.page.scss'],
  standalone: false
})
export class RegistrarFichajePage implements OnInit {
  usuarioActual: Usuario | null = null;
  trabajos: Trabajo[] = [];
  fichajeActivo: Fichaje | null = null;

  idTrabajoSeleccionado: number | null = null;
  latitud: number | null = null;
  longitud: number | null = null;
  direccionGeorreferenciada = '';

  cargando = true;
  procesandoFichaje = false;

  constructor(
    private api: ApiService,
    private toastCtrl: ToastController,
    private router: Router
  ) {}

  ngOnInit() {
    this.cargarUsuario();
    this.cargarDatos();
  }

  ionViewWillEnter() {
    this.cargarUsuario();
    this.cargarDatos();
  }

  cargarUsuario() {
    const raw = localStorage.getItem('auth_user') || localStorage.getItem('empleado_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }
    this.usuarioActual = JSON.parse(raw);
  }

  async cargarDatos() {
    if (!this.usuarioActual) return;
    this.cargando = true;

    // Cargar trabajos disponibles (creados en AppAdmin)
    this.api.getTrabajos().subscribe({
      next: (t) => {
        this.trabajos = t;
        if (t.length > 0 && !this.idTrabajoSeleccionado) {
          this.idTrabajoSeleccionado = t[0].IdTrabajo;
        }
      },
      error: (e) => console.warn('Error al cargar trabajos:', e)
    });

    // Comprobar si hay fichaje abierto en las ultimas 12 horas
    this.api.getUltimoFichajeActivo(this.usuarioActual.IdUsuario).subscribe({
      next: async (f) => {
        this.fichajeActivo = f;
        this.cargando = false;
        if (!f) {
          await this.obtenerUbicacionGPS();
        }
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  async obtenerUbicacionGPS(): Promise<void> {
    return new Promise((resolve) => {
      // Intento 1: API de Geolocalizacion HTML5 nativa del navegador / PWA
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            this.latitud = pos.coords.latitude;
            this.longitud = pos.coords.longitude;
            this.resolverDireccionNominatim();
            resolve();
          },
          async () => {
            await this.fallbackCapacitorGps(resolve);
          },
          { enableHighAccuracy: true, timeout: 6000 }
        );
      } else {
        this.fallbackCapacitorGps(resolve);
      }
    });
  }

  private async fallbackCapacitorGps(resolve: () => void) {
    try {
      const pos = await Geolocation.getCurrentPosition({ enableHighAccuracy: true, timeout: 6000 });
      this.latitud = pos.coords.latitude;
      this.longitud = pos.coords.longitude;
      this.resolverDireccionNominatim();
    } catch {
      // Coordenadas fijas de demostracion (Campus Universidad de Alicante)
      this.latitud = 38.38735;
      this.longitud = -0.51238;
      this.direccionGeorreferenciada = 'Universidad de Alicante, San Vicente del Raspeig';
    }
    resolve();
  }

  private resolverDireccionNominatim() {
    if (!this.latitud || !this.longitud) return;
    this.api.getDireccionNominatim(this.latitud, this.longitud).subscribe({
      next: (res) => {
        this.direccionGeorreferenciada = res.display_name || `Lat: ${this.latitud}, Lon: ${this.longitud}`;
      },
      error: () => {
        this.direccionGeorreferenciada = `Lat: ${this.latitud}, Lon: ${this.longitud}`;
      }
    });
  }

  async registrarEntrada() {
    if (!this.usuarioActual || !this.idTrabajoSeleccionado) {
      const t = await this.toastCtrl.create({
        message: 'Por favor, selecciona un trabajo asignado',
        duration: 2500,
        color: 'warning'
      });
      t.present();
      return;
    }
    this.procesandoFichaje = true;

    if (!this.latitud || !this.longitud) {
      await this.obtenerUbicacionGPS();
    }

    const payload = {
      IdUsuario: this.usuarioActual.IdUsuario,
      IdTrabajo: this.idTrabajoSeleccionado,
      GeolocalizacionLatitud: this.latitud || 38.38735,
      GeolocalizacionLongitud: this.longitud || -0.51238
    };

    this.api.iniciarFichaje(payload).subscribe({
      next: async (res) => {
        this.procesandoFichaje = false;
        const toast = await this.toastCtrl.create({
          message: 'Fichaje de entrada registrado correctamente',
          duration: 3000,
          color: 'success'
        });
        await toast.present();
        this.cargarDatos();
      },
      error: async (err) => {
        this.procesandoFichaje = false;
        const toast = await this.toastCtrl.create({
          message: err.error?.message || 'Error al registrar el fichaje de entrada',
          duration: 3500,
          color: 'danger'
        });
        await toast.present();
      }
    });
  }

  async registrarSalida() {
    if (!this.fichajeActivo) return;
    this.procesandoFichaje = true;

    this.api.cerrarFichaje(this.fichajeActivo.IdFichaje).subscribe({
      next: async (fichajeCerrado) => {
        this.procesandoFichaje = false;
        const horas = fichajeCerrado.HorasTrabajadas || 0;
        const toast = await this.toastCtrl.create({
          message: `Fichaje finalizado con exito. Total horas computadas: ${horas}h`,
          duration: 4000,
          color: 'success'
        });
        await toast.present();
        this.fichajeActivo = null;
        this.cargarDatos();
      },
      error: async (err) => {
        this.procesandoFichaje = false;
        const toast = await this.toastCtrl.create({
          message: err.error?.message || 'Error al cerrar el fichaje',
          duration: 3500,
          color: 'danger'
        });
        await toast.present();
      }
    });
  }
}

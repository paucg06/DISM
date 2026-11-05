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
    const raw = localStorage.getItem('empleado_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }
    this.usuarioActual = JSON.parse(raw);
    this.cargarDatos();
  }

  ionViewWillEnter() {
    this.cargarDatos();
  }

  async cargarDatos() {
    if (!this.usuarioActual) return;
    this.cargando = true;

    // Cargar trabajos disponibles
    this.api.getTrabajos().subscribe(t => {
      this.trabajos = t;
      if (t.length > 0 && !this.idTrabajoSeleccionado) {
        this.idTrabajoSeleccionado = t[0].IdTrabajo;
      }
    });

    // Comprobar si hay fichaje abierto en las últimas 12 horas
    this.api.getUltimoFichajeActivo(this.usuarioActual.IdUsuario).subscribe({
      next: async (f) => {
        this.fichajeActivo = f;
        this.cargando = false;
        if (!f) {
          // Si no tiene fichaje previo, obtenemos geolocalización preventiva para fichar entrada
          await this.obtenerUbicacionGPS();
        }
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  async obtenerUbicacionGPS() {
    try {
      const pos = await Geolocation.getCurrentPosition({ enableHighAccuracy: true, timeout: 8000 });
      this.latitud = pos.coords.latitude;
      this.longitud = pos.coords.longitude;

      this.api.getDireccionNominatim(this.latitud, this.longitud).subscribe({
        next: (res) => {
          this.direccionGeorreferenciada = res.display_name || '';
        },
        error: () => {
          this.direccionGeorreferenciada = 'Ubicación GPS registrada correctamente';
        }
      });
    } catch (e) {
      // Coordenadas fijas por defecto (Alicante - Campus Universidad) si falla el permiso de GPS del navegador
      this.latitud = 38.38735;
      this.longitud = -0.51238;
      this.direccionGeorreferenciada = 'Universidad de Alicante, San Vicente del Raspeig';
    }
  }

  async registrarEntrada() {
    if (!this.usuarioActual || !this.idTrabajoSeleccionado) {
      const t = await this.toastCtrl.create({ message: 'Por favor, selecciona un trabajo', duration: 2500, color: 'warning' });
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
          message: '¡Fichaje de entrada registrado correctamente!',
          duration: 3000,
          color: 'success'
        });
        await toast.present();
        this.cargarDatos();
      },
      error: async (err) => {
        this.procesandoFichaje = false;
        const toast = await this.toastCtrl.create({
          message: err.error?.message || 'Error al registrar entrada',
          duration: 3000,
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
      next: async (res) => {
        this.procesandoFichaje = false;
        const toast = await this.toastCtrl.create({
          message: `¡Fichaje finalizado! Horas computadas: ${res.HorasTrabajadas || 1} hora(s).`,
          duration: 4000,
          color: 'success'
        });
        await toast.present();
        this.cargarDatos();
      },
      error: async (err) => {
        this.procesandoFichaje = false;
        const toast = await this.toastCtrl.create({
          message: err.error?.message || 'Error al finalizar fichaje',
          duration: 3000,
          color: 'danger'
        });
        await toast.present();
      }
    });
  }
}

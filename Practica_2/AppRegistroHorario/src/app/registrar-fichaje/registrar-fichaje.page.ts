import { Component, OnInit } from '@angular/core';
import { ApiService, Fichaje, Trabajo, Usuario } from '../services/api';
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
    this.cargarDatos();
  }

  ionViewWillEnter() {
    this.cargarDatos();
  }

  cargarUsuario(): boolean {
    const raw = localStorage.getItem('auth_user');
    if (!raw) {
      this.router.navigate(['/login'], { replaceUrl: true });
      return false;
    }
    this.usuarioActual = JSON.parse(raw);
    return true;
  }

  cargarDatos() {
    if (!this.cargarUsuario()) return;
    this.cargando = true;

    // Timeout de seguridad de 2 segundos para evitar bloqueo en la interfaz
    const safetyTimeout = setTimeout(() => {
      this.cargando = false;
      this.obtenerUbicacionGPS();
    }, 2000);

    // Cargar trabajos
    this.api.getTrabajos().subscribe({
      next: (t) => {
        this.trabajos = t;
        if (t.length > 0 && !this.idTrabajoSeleccionado) {
          this.idTrabajoSeleccionado = t[0].IdTrabajo;
        }
      },
      error: () => {}
    });

    // Comprobar si hay fichaje activo en < 12 horas
    this.api.getUltimoFichajeActivo(this.usuarioActual!.IdUsuario).subscribe({
      next: (f) => {
        clearTimeout(safetyTimeout);
        this.fichajeActivo = f;
        this.cargando = false;
        if (!f) {
          this.obtenerUbicacionGPS();
        }
      },
      error: () => {
        clearTimeout(safetyTimeout);
        this.cargando = false;
        this.obtenerUbicacionGPS();
      }
    });
  }

  obtenerUbicacionGPS() {
    if (this.latitud && this.longitud) return;

    if (navigator && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          this.latitud = pos.coords.latitude;
          this.longitud = pos.coords.longitude;
          this.resolverDireccionNominatim();
        },
        () => {
          this.asignarCoordenadasFallback();
        },
        { enableHighAccuracy: false, timeout: 3500 }
      );
    } else {
      this.asignarCoordenadasFallback();
    }
  }

  asignarCoordenadasFallback() {
    this.latitud = 38.38735;
    this.longitud = -0.51238;
    this.direccionGeorreferenciada = 'Universidad de Alicante, San Vicente del Raspeig';
  }

  resolverDireccionNominatim() {
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
      await t.present();
      return;
    }

    this.procesandoFichaje = true;
    const datos = {
      IdUsuario: this.usuarioActual.IdUsuario,
      IdTrabajo: this.idTrabajoSeleccionado,
      GeolocalizacionLatitud: this.latitud || 38.38735,
      GeolocalizacionLongitud: this.longitud || -0.51238
    };

    this.api.iniciarFichaje(datos).subscribe({
      next: async (nuevo) => {
        this.procesandoFichaje = false;
        this.fichajeActivo = nuevo;
        const toast = await this.toastCtrl.create({
          message: 'Entrada registrada exitosamente.',
          duration: 3000,
          color: 'success'
        });
        await toast.present();
        this.cargarDatos();
      },
      error: async (err) => {
        this.procesandoFichaje = false;
        const toast = await this.toastCtrl.create({
          message: err.error?.message || 'Error al registrar la entrada.',
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
      next: async (cerrado) => {
        this.procesandoFichaje = false;
        this.fichajeActivo = null;
        const toast = await this.toastCtrl.create({
          message: `Salida registrada. Horas trabajadas: ${cerrado.HorasTrabajadas || 0}h`,
          duration: 3500,
          color: 'success'
        });
        await toast.present();
        this.cargarDatos();
      },
      error: async (err) => {
        this.procesandoFichaje = false;
        const toast = await this.toastCtrl.create({
          message: err.error?.message || 'Error al registrar la salida.',
          duration: 3000,
          color: 'danger'
        });
        await toast.present();
      }
    });
  }

  logout() {
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}

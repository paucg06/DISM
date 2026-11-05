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

  idTrabajoSeleccionado: number = 1;
  latitud: number = 38.38735;
  longitud: number = -0.51238;
  direccionGeorreferenciada: string = 'Universidad de Alicante, San Vicente del Raspeig';

  cargando: boolean = false;
  procesandoFichaje: boolean = false;

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

    // Cargar trabajos
    this.api.getTrabajos().subscribe({
      next: (t) => {
        if (t && t.length > 0) {
          this.trabajos = t;
          if (!this.idTrabajoSeleccionado) {
            this.idTrabajoSeleccionado = t[0].IdTrabajo;
          }
        }
      },
      error: () => {}
    });

    // Comprobar si hay fichaje activo en < 12 horas
    this.api.getUltimoFichajeActivo(this.usuarioActual!.IdUsuario).subscribe({
      next: (f) => {
        this.fichajeActivo = f;
      },
      error: () => {
        this.fichajeActivo = null;
      }
    });

    // Intentar geolocalización en segundo plano sin bloquear
    this.obtenerUbicacionGPS();
  }

  obtenerUbicacionGPS() {
    if (navigator && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          this.latitud = pos.coords.latitude;
          this.longitud = pos.coords.longitude;
          this.resolverDireccionNominatim();
        },
        () => {
          // Si falla o no hay permiso, se mantienen las coordenadas predeterminadas de la UA
        },
        { enableHighAccuracy: false, timeout: 2500 }
      );
    }
  }

  resolverDireccionNominatim() {
    if (!this.latitud || !this.longitud) return;
    this.api.getDireccionNominatim(this.latitud, this.longitud).subscribe({
      next: (res) => {
        if (res && res.display_name) {
          this.direccionGeorreferenciada = res.display_name;
        }
      },
      error: () => {}
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
      IdTrabajo: Number(this.idTrabajoSeleccionado),
      GeolocalizacionLatitud: this.latitud,
      GeolocalizacionLongitud: this.longitud
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

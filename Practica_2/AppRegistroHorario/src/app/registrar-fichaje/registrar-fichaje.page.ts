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
  fichajesActivos: Fichaje[] = [];

  idTrabajoSeleccionado: number = 1;
  latitud: number = 38.38735;
  longitud: number = -0.51238;

  procesandoFichaje: boolean = false;
  fichajeCerrandoId: number | null = null;

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

    // Cargar catálogo de trabajos
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

    // Cargar fichajes activos en paralelo
    this.cargarFichajesActivos();

    // Actualizar coordenadas GPS en segundo plano
    this.obtenerUbicacionGPS();
  }

  cargarFichajesActivos() {
    if (!this.usuarioActual) return;
    this.api.getFichajesActivos(this.usuarioActual.IdUsuario).subscribe({
      next: (lista) => {
        this.fichajesActivos = lista || [];
      },
      error: () => {
        this.fichajesActivos = [];
      }
    });
  }

  obtenerUbicacionGPS() {
    if (navigator && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          this.latitud = pos.coords.latitude;
          this.longitud = pos.coords.longitude;
        },
        () => {},
        { enableHighAccuracy: false, timeout: 2000 }
      );
    }
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
        // Asignar nombre del trabajo si viniese vacío
        if (!nuevo.NombreTrabajo) {
          const trab = this.trabajos.find(t => t.IdTrabajo === Number(this.idTrabajoSeleccionado));
          nuevo.NombreTrabajo = trab ? trab.Nombre : `Trabajo #${this.idTrabajoSeleccionado}`;
        }
        // Añadir inmediatamente debajo al listado de turnos activos en paralelo
        this.fichajesActivos.unshift(nuevo);

        const toast = await this.toastCtrl.create({
          message: `Entrada iniciada para: ${nuevo.NombreTrabajo}`,
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

  async finalizarFichaje(fichaje: Fichaje) {
    this.fichajeCerrandoId = fichaje.IdFichaje;
    this.api.cerrarFichaje(fichaje.IdFichaje).subscribe({
      next: async (cerrado) => {
        this.fichajeCerrandoId = null;
        // Eliminar inmediatamente de la lista visible de turnos en curso
        this.fichajesActivos = this.fichajesActivos.filter(f => f.IdFichaje !== fichaje.IdFichaje);

        const toast = await this.toastCtrl.create({
          message: `Salida registrada en ${fichaje.NombreTrabajo}. Horas trabajadas: ${cerrado.HorasTrabajadas || 1}h`,
          duration: 3500,
          color: 'success'
        });
        await toast.present();
      },
      error: async (err) => {
        this.fichajeCerrandoId = null;
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

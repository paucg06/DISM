import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
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

  constructor(
    private api: ApiService,
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
          this.cdr.detectChanges();
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
        this.cdr.detectChanges();
      },
      error: () => {
        this.fichajesActivos = [];
        this.cdr.detectChanges();
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

    const idTrabajo = Number(this.idTrabajoSeleccionado);
    const trab = this.trabajos.find(t => t.IdTrabajo === idTrabajo);
    const nombreTrabajo = trab ? trab.Nombre : `Trabajo #${idTrabajo}`;

    const pad = (n: number) => String(n).padStart(2, '0');
    const d = new Date();
    const fechaHoraEntrada = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;

    // 1. Inserción inmediata en pantalla (en ese preciso instante, 0 ms)
    const fichajeVisual: Fichaje = {
      IdFichaje: Date.now(),
      FechaHoraEntrada: fechaHoraEntrada,
      FechaHoraSalida: null,
      HorasTrabajadas: null,
      IdTrabajo: idTrabajo,
      NombreTrabajo: nombreTrabajo,
      IdUsuario: this.usuarioActual.IdUsuario,
      NombreUsuario: this.usuarioActual.Nombre,
      GeolocalizacionLatitud: this.latitud,
      GeolocalizacionLongitud: this.longitud
    };

    this.fichajesActivos = [fichajeVisual, ...this.fichajesActivos];
    this.cdr.detectChanges();

    // Notificación de entrada iniciada
    const toast = await this.toastCtrl.create({
      message: `Entrada iniciada para: ${nombreTrabajo}`,
      duration: 3000,
      color: 'success'
    });
    await toast.present();

    // 2. Persistir en el servidor en segundo plano
    const datos = {
      IdUsuario: this.usuarioActual.IdUsuario,
      IdTrabajo: idTrabajo,
      GeolocalizacionLatitud: this.latitud,
      GeolocalizacionLongitud: this.longitud
    };

    this.api.iniciarFichaje(datos).subscribe({
      next: (guardado) => {
        if (guardado && guardado.IdFichaje) {
          fichajeVisual.IdFichaje = guardado.IdFichaje;
          this.cdr.detectChanges();
        }
      },
      error: () => {}
    });
  }

  async finalizarFichaje(fichaje: Fichaje) {
    const idCerrar = fichaje.IdFichaje;
    const nombreTrab = fichaje.NombreTrabajo || 'Tarea';

    // 1. Eliminar inmediatamente el recuadro de la vista (en ese preciso instante)
    this.fichajesActivos = this.fichajesActivos.filter(f => f.IdFichaje !== idCerrar);
    this.cdr.detectChanges();

    // 2. Notificación verde de finalización
    const toast = await this.toastCtrl.create({
      message: `El fichaje ha finalizado para: ${nombreTrab}`,
      duration: 3000,
      color: 'success'
    });
    await toast.present();

    // 3. Persistir en la base de datos en segundo plano
    this.api.cerrarFichaje(idCerrar).subscribe({
      next: () => {},
      error: () => {}
    });
  }

  logout() {
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}

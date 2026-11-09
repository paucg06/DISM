import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService, Trabajo } from '../services/api';
import { AlertController, ToastController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-trabajos',
  templateUrl: './trabajos.page.html',
  styleUrls: ['./trabajos.page.scss'],
  standalone: false
})
export class TrabajosPage implements OnInit {
  trabajos: Trabajo[] = [];
  cargando = false;
  trabajoSeleccionado: Trabajo | null = null;
  mostrarModal = false;

  constructor(
    private api: ApiService,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.cargarTrabajos();
  }

  ionViewWillEnter() {
    this.cargarTrabajos();
  }

  cargarTrabajos() {
    this.cargando = true;
    this.cdr.detectChanges();
    this.api.getTrabajos().subscribe({
      next: (data) => {
        this.trabajos = [...(data || [])];
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });
  }

  verDetalle(trabajo: Trabajo) {
    this.trabajoSeleccionado = { ...trabajo };
    this.mostrarModal = true;
  }

  nuevoTrabajo() {
    const nextId = this.trabajos.length > 0 ? Math.max(...this.trabajos.map(t => t.IdTrabajo)) + 1 : 1;
    this.trabajoSeleccionado = {
      IdTrabajo: nextId,
      Nombre: ''
    };
    this.mostrarModal = true;
  }

  cerrarModal() {
    this.mostrarModal = false;
    this.trabajoSeleccionado = null;
  }

  async guardarTrabajo() {
    if (!this.trabajoSeleccionado || !this.trabajoSeleccionado.Nombre || !this.trabajoSeleccionado.IdTrabajo) {
      const toast = await this.toastCtrl.create({
        message: 'El ID y el Nombre del trabajo son obligatorios',
        duration: 2500,
        color: 'warning'
      });
      await toast.present();
      return;
    }

    const existe = this.trabajos.some(t => t.IdTrabajo === this.trabajoSeleccionado!.IdTrabajo);
    if (existe) {
      this.api.actualizarTrabajo(this.trabajoSeleccionado.IdTrabajo, this.trabajoSeleccionado).subscribe({
        next: async () => {
          this.cerrarModal();
          this.cargarTrabajos();
          const t = await this.toastCtrl.create({ message: 'Trabajo actualizado', duration: 2000, color: 'success' });
          await t.present();
        },
        error: async (err) => {
          const t = await this.toastCtrl.create({ message: err.error?.message || 'Error al actualizar', duration: 3000, color: 'danger' });
          await t.present();
        }
      });
    } else {
      this.api.crearTrabajo(this.trabajoSeleccionado).subscribe({
        next: async () => {
          this.cerrarModal();
          this.cargarTrabajos();
          const t = await this.toastCtrl.create({ message: 'Trabajo creado', duration: 2000, color: 'success' });
          await t.present();
        },
        error: async (err) => {
          const t = await this.toastCtrl.create({ message: err.error?.message || 'Error al crear trabajo', duration: 3000, color: 'danger' });
          await t.present();
        }
      });
    }
  }

  async confirmarEliminar(id: number) {
    const alert = await this.alertCtrl.create({
      header: 'Confirmar Eliminación',
      message: '¿Estás seguro de que deseas eliminar este trabajo?',
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        {
          text: 'Eliminar',
          role: 'destructive',
          handler: () => {
            this.api.eliminarTrabajo(id).subscribe({
              next: async () => {
                this.cargarTrabajos();
                const t = await this.toastCtrl.create({ message: 'Trabajo eliminado', duration: 2000, color: 'success' });
                await t.present();
              },
              error: async (err) => {
                const t = await this.toastCtrl.create({ message: err.error?.message || 'Error al eliminar', duration: 3000, color: 'danger' });
                await t.present();
              }
            });
          }
        }
      ]
    });
    await alert.present();
  }

  logout() {
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}

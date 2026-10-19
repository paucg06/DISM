import { Component, OnInit } from '@angular/core';
import { ApiService, Trabajo } from '../services/api';
import { AlertController, ToastController } from '@ionic/angular';

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
    private toastCtrl: ToastController
  ) {}

  ngOnInit() {
    this.cargarTrabajos();
  }

  cargarTrabajos() {
    this.cargando = true;
    this.api.getTrabajos().subscribe({
      next: (data) => {
        this.trabajos = data;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
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

  guardarTrabajo() {
    if (!this.trabajoSeleccionado || !this.trabajoSeleccionado.Nombre) return;
    const existe = this.trabajos.some(t => t.IdTrabajo === this.trabajoSeleccionado!.IdTrabajo);
    if (existe) {
      this.api.actualizarTrabajo(this.trabajoSeleccionado.IdTrabajo, this.trabajoSeleccionado).subscribe({
        next: async () => {
          this.cerrarModal();
          this.cargarTrabajos();
          const t = await this.toastCtrl.create({ message: 'Trabajo actualizado correctamente', duration: 2000, color: 'success' });
          t.present();
        }
      });
    } else {
      this.api.crearTrabajo(this.trabajoSeleccionado).subscribe({
        next: async () => {
          this.cerrarModal();
          this.cargarTrabajos();
          const t = await this.toastCtrl.create({ message: 'Trabajo creado exitosamente', duration: 2000, color: 'success' });
          t.present();
        }
      });
    }
  }

  async confirmarEliminar(id: number) {
    const alert = await this.alertCtrl.create({
      header: 'Confirmar eliminación',
      message: '¿Estás seguro de que deseas eliminar este trabajo?',
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        {
          text: 'Eliminar',
          handler: () => {
            this.api.eliminarTrabajo(id).subscribe({
              next: () => {
                this.cerrarModal();
                this.cargarTrabajos();
              }
            });
          }
        }
      ]
    });
    await alert.present();
  }
}

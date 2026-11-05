import { Component, OnInit } from '@angular/core';
import { ApiService, Usuario } from '../services/api';
import { AlertController, ToastController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-usuarios',
  templateUrl: './usuarios.page.html',
  styleUrls: ['./usuarios.page.scss'],
  standalone: false
})
export class UsuariosPage implements OnInit {
  usuarios: Usuario[] = [];
  cargando = false;
  usuarioSeleccionado: Usuario | null = null;
  mostrarModal = false;
  modoEdicion = false;

  constructor(
    private api: ApiService,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController,
    private router: Router
  ) {}

  ngOnInit() {
    this.cargarUsuarios();
  }

  ionViewWillEnter() {
    this.cargarUsuarios();
  }

  cargarUsuarios() {
    this.cargando = true;
    this.api.getUsuarios().subscribe({
      next: (data) => {
        this.usuarios = data || [];
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  verDetalle(usuario: Usuario) {
    this.usuarioSeleccionado = { ...usuario };
    this.modoEdicion = true;
    this.mostrarModal = true;
  }

  nuevoUsuario() {
    const nextId = this.usuarios.length > 0 ? Math.max(...this.usuarios.map(u => u.IdUsuario)) + 1 : 1;
    this.usuarioSeleccionado = {
      IdUsuario: nextId,
      Nombre: '',
      Usuario: '',
      Clave: '',
      Rol: 'empleado'
    };
    this.modoEdicion = false;
    this.mostrarModal = true;
  }

  cerrarModal() {
    this.mostrarModal = false;
    this.usuarioSeleccionado = null;
  }

  async guardarUsuario() {
    if (!this.usuarioSeleccionado || !this.usuarioSeleccionado.Nombre || !this.usuarioSeleccionado.IdUsuario) {
      const toast = await this.toastCtrl.create({
        message: 'El ID y el Nombre son obligatorios',
        duration: 2500,
        color: 'warning'
      });
      await toast.present();
      return;
    }

    if (this.modoEdicion) {
      this.api.actualizarUsuario(this.usuarioSeleccionado.IdUsuario, this.usuarioSeleccionado).subscribe({
        next: async () => {
          this.cerrarModal();
          this.cargarUsuarios();
          const t = await this.toastCtrl.create({ message: 'Usuario actualizado con éxito', duration: 2000, color: 'success' });
          await t.present();
        },
        error: async (err) => {
          const t = await this.toastCtrl.create({ message: err.error?.message || 'Error al actualizar', duration: 3000, color: 'danger' });
          await t.present();
        }
      });
    } else {
      this.api.crearUsuario(this.usuarioSeleccionado).subscribe({
        next: async () => {
          this.cerrarModal();
          this.cargarUsuarios();
          const t = await this.toastCtrl.create({ message: 'Usuario creado con éxito', duration: 2000, color: 'success' });
          await t.present();
        },
        error: async (err) => {
          const t = await this.toastCtrl.create({ message: err.error?.message || 'Error al crear usuario', duration: 3000, color: 'danger' });
          await t.present();
        }
      });
    }
  }

  async confirmarEliminar(id: number) {
    const alert = await this.alertCtrl.create({
      header: 'Confirmar Eliminación',
      message: '¿Estás seguro de que deseas eliminar este usuario?',
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        {
          text: 'Eliminar',
          role: 'destructive',
          handler: () => {
            this.api.eliminarUsuario(id).subscribe({
              next: async () => {
                this.cargarUsuarios();
                const t = await this.toastCtrl.create({ message: 'Usuario eliminado', duration: 2000, color: 'success' });
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

import { Component, OnInit } from '@angular/core';
import { ApiService, Usuario } from '../services/api';
import { AlertController, ToastController } from '@ionic/angular';

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

  constructor(
    private api: ApiService,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController
  ) {}

  ngOnInit() {
    this.cargarUsuarios();
  }

  cargarUsuarios() {
    this.cargando = true;
    this.api.getUsuarios().subscribe({
      next: (data) => {
        this.usuarios = data;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  verDetalle(usuario: Usuario) {
    this.usuarioSeleccionado = { ...usuario };
    this.mostrarModal = true;
  }

  nuevoUsuario() {
    const nextId = this.usuarios.length > 0 ? Math.max(...this.usuarios.map(u => u.IdUsuario)) + 1 : 1;
    this.usuarioSeleccionado = {
      IdUsuario: nextId,
      Nombre: '',
      Usuario: '',
      Clave: '1234',
      Rol: 'empleado'
    };
    this.mostrarModal = true;
  }

  cerrarModal() {
    this.mostrarModal = false;
    this.usuarioSeleccionado = null;
  }

  guardarUsuario() {
    if (!this.usuarioSeleccionado || !this.usuarioSeleccionado.Nombre || !this.usuarioSeleccionado.Usuario) {
      return;
    }
    const existe = this.usuarios.some(u => u.IdUsuario === this.usuarioSeleccionado!.IdUsuario);
    if (existe) {
      this.api.actualizarUsuario(this.usuarioSeleccionado.IdUsuario, this.usuarioSeleccionado).subscribe({
        next: async () => {
          this.cerrarModal();
          this.cargarUsuarios();
          const t = await this.toastCtrl.create({ message: 'Usuario actualizado correctamente', duration: 2000, color: 'success' });
          t.present();
        }
      });
    } else {
      this.api.crearUsuario(this.usuarioSeleccionado).subscribe({
        next: async () => {
          this.cerrarModal();
          this.cargarUsuarios();
          const t = await this.toastCtrl.create({ message: 'Usuario creado exitosamente', duration: 2000, color: 'success' });
          t.present();
        }
      });
    }
  }

  async confirmarEliminar(id: number) {
    const alert = await this.alertCtrl.create({
      header: 'Confirmar eliminación',
      message: '¿Estás seguro de que deseas eliminar este usuario?',
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        {
          text: 'Eliminar',
          handler: () => {
            this.api.eliminarUsuario(id).subscribe({
              next: () => {
                this.cerrarModal();
                this.cargarUsuarios();
              }
            });
          }
        }
      ]
    });
    await alert.present();
  }
}

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService, Usuario } from '../services/api';
import { ToastController } from '@ionic/angular';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: false
})
export class LoginPage implements OnInit {
  usuario = 'admin';
  clave = 'admin123';
  cargando = false;
  showInstallBtn = false;
  deferredPrompt: any = null;

  constructor(
    private api: ApiService,
    private router: Router,
    private toastCtrl: ToastController
  ) {}

  ngOnInit() {
    window.addEventListener('beforeinstallprompt', (e: any) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallBtn = true;
    });
  }

  fillAdmin() {
    this.usuario = 'admin';
    this.clave = 'admin123';
    this.onLogin();
  }

  fillEmpleado() {
    this.usuario = 'sergio';
    this.clave = '1234';
    this.onLogin();
  }

  async onLogin() {
    if (!this.usuario || !this.clave) {
      const toast = await this.toastCtrl.create({
        message: 'Por favor, introduce usuario y contraseña',
        duration: 2500,
        color: 'warning'
      });
      await toast.present();
      return;
    }

    this.cargando = true;
    this.api.login(this.usuario, this.clave).subscribe({
      next: async (user: Usuario) => {
        this.cargando = false;
        localStorage.setItem('auth_user', JSON.stringify(user));
        localStorage.setItem('admin_user', JSON.stringify(user));
        localStorage.setItem('empleado_user', JSON.stringify(user));

        const role = user.Rol || (user.Usuario === 'admin' ? 'admin' : 'empleado');

        // Aplicar el tema dinamico: Azul para Admin, Verde para Empleado
        if (role === 'admin') {
          document.body.classList.remove('theme-empleado');
          document.body.classList.add('theme-admin');
          const toast = await this.toastCtrl.create({
            message: `Bienvenido Administrador ${user.Nombre}. Modo Azul activado.`,
            duration: 2500,
            color: 'primary'
          });
          await toast.present();
          this.router.navigate(['/tabs/usuarios']);
        } else {
          document.body.classList.remove('theme-admin');
          document.body.classList.add('theme-empleado');
          const toast = await this.toastCtrl.create({
            message: `Bienvenido Empleado ${user.Nombre}. Modo Verde activado.`,
            duration: 2500,
            color: 'success'
          });
          await toast.present();
          this.router.navigate(['/tabs/registrar-fichaje']);
        }
      },
      error: async (err) => {
        this.cargando = false;
        const toast = await this.toastCtrl.create({
          message: err.error?.message || 'Usuario o contraseña incorrectos',
          duration: 3000,
          color: 'danger'
        });
        await toast.present();
      }
    });
  }

  installPwa() {
    if (this.deferredPrompt) {
      this.deferredPrompt.prompt();
      this.deferredPrompt.userChoice.then(() => {
        this.deferredPrompt = null;
        this.showInstallBtn = false;
      });
    }
  }
}

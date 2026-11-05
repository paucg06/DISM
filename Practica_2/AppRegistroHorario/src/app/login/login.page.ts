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
  usuario = '';
  clave = '';
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

  async onLogin() {
    if (!this.usuario || !this.clave) {
      const toast = await this.toastCtrl.create({
        message: 'Por favor, introduce tu usuario y contraseña',
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

        const toast = await this.toastCtrl.create({
          message: `Bienvenido, ${user.Nombre}`,
          duration: 2000,
          color: 'success'
        });
        await toast.present();

        if (role === 'admin') {
          this.router.navigate(['/tabs/usuarios']);
        } else {
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

  async installPwa() {
    if (this.deferredPrompt) {
      this.deferredPrompt.prompt();
      const choiceResult = await this.deferredPrompt.userChoice;
      if (choiceResult.outcome === 'accepted') {
        this.showInstallBtn = false;
      }
      this.deferredPrompt = null;
    }
  }
}

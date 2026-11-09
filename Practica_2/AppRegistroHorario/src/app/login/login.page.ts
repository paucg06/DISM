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

  constructor(
    private api: ApiService,
    private router: Router,
    private toastCtrl: ToastController
  ) {}

  ngOnInit() {}

  ionViewWillEnter() {
    this.usuario = '';
    this.clave = '';
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
        // Guardar sesión activa en localStorage
        localStorage.removeItem('auth_user');
        sessionStorage.removeItem('auth_user');
        localStorage.setItem('auth_user', JSON.stringify(user));

        const toast = await this.toastCtrl.create({
          message: `Bienvenido, ${user.Nombre}`,
          duration: 2000,
          color: 'success'
        });
        await toast.present();

        this.router.navigate(['/home'], { replaceUrl: true });
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
}

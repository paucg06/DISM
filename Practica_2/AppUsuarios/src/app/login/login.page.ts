import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../services/api';
import { ToastController } from '@ionic/angular';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: false
})
export class LoginPage implements OnInit {
  usuario = 'sergio';
  clave = '1234';
  cargando = false;

  constructor(
    private api: ApiService,
    private router: Router,
    private toastCtrl: ToastController
  ) {}

  ngOnInit() {}

  async onLogin() {
    this.cargando = true;
    this.api.login(this.usuario, this.clave).subscribe({
      next: (user) => {
        this.cargando = false;
        localStorage.setItem('empleado_user', JSON.stringify(user));
        this.router.navigate(['/home']);
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

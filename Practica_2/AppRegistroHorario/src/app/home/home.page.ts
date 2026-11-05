import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: false
})
export class HomePage implements OnInit {
  userName = 'Usuario';
  userRole = 'empleado';
  userObj: any = null;

  constructor(private router: Router) {}

  ngOnInit() {
    this.cargarDatos();
  }

  ionViewWillEnter() {
    this.cargarDatos();
  }

  cargarDatos() {
    const raw = localStorage.getItem('auth_user') || localStorage.getItem('admin_user') || localStorage.getItem('empleado_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }
    this.userObj = JSON.parse(raw);
    this.userName = this.userObj.Nombre || 'Usuario';
    this.userRole = this.userObj.Rol || (this.userObj.Usuario === 'admin' ? 'admin' : 'empleado');
  }

  logout() {
    localStorage.removeItem('auth_user');
    localStorage.removeItem('admin_user');
    localStorage.removeItem('empleado_user');
    document.body.classList.remove('theme-admin', 'theme-empleado');
    this.router.navigate(['/login']);
  }
}

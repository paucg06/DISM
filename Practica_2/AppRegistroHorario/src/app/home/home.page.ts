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
    const raw = localStorage.getItem('auth_user');
    if (!raw) {
      this.router.navigate(['/login'], { replaceUrl: true });
      return;
    }
    this.userObj = JSON.parse(raw);
    this.userName = this.userObj.Nombre || 'Usuario';
    this.userRole = (this.userObj.Rol === 'admin' || this.userObj.Usuario === 'admin') ? 'admin' : 'empleado';
  }

  logout() {
    localStorage.clear();
    sessionStorage.clear();
    this.userObj = null;
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}

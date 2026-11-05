import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: false
})
export class HomePage implements OnInit {
  empleadoName = 'Empleado';

  constructor(private router: Router) {}

  ngOnInit() {
    const raw = localStorage.getItem('empleado_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }
    const user = JSON.parse(raw);
    this.empleadoName = user.Nombre || 'Empleado';
  }

  logout() {
    localStorage.removeItem('empleado_user');
    this.router.navigate(['/login']);
  }
}

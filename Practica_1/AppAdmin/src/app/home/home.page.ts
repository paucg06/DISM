import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: false
})
export class HomePage implements OnInit {
  adminName = 'Administrador';

  constructor(private router: Router) {}

  ngOnInit() {
    const raw = localStorage.getItem('admin_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }
    const user = JSON.parse(raw);
    this.adminName = user.Nombre || 'Administrador';
  }

  logout() {
    localStorage.removeItem('admin_user');
    this.router.navigate(['/login']);
  }
}

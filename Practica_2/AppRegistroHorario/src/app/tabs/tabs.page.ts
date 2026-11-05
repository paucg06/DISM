import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tabs',
  templateUrl: './tabs.page.html',
  styleUrls: ['./tabs.page.scss'],
  standalone: false
})
export class TabsPage implements OnInit {
  currentUser: any = null;
  role: 'admin' | 'empleado' = 'admin';

  constructor(private router: Router) {}

  ngOnInit() {
    this.checkAuth();
  }

  ionViewWillEnter() {
    this.checkAuth();
  }

  checkAuth() {
    const raw = localStorage.getItem('auth_user') || localStorage.getItem('admin_user') || localStorage.getItem('empleado_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }
    this.currentUser = JSON.parse(raw);
    this.role = (this.currentUser.Rol === 'admin' || this.currentUser.Usuario === 'admin') ? 'admin' : 'empleado';
  }

  logout() {
    localStorage.removeItem('auth_user');
    localStorage.removeItem('admin_user');
    localStorage.removeItem('empleado_user');
    this.router.navigate(['/login']);
  }
}

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
  showInstallBtn = false;
  deferredPrompt: any = null;

  constructor(private router: Router) {}

  ngOnInit() {
    this.checkAuth();
    window.addEventListener('beforeinstallprompt', (e: any) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallBtn = true;
    });
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

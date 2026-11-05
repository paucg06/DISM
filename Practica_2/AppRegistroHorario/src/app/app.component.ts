import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
  standalone: false,
})
export class AppComponent implements OnInit {
  constructor() {}

  ngOnInit() {
    this.restaurarTemaActivo();
  }

  restaurarTemaActivo() {
    const raw = localStorage.getItem('auth_user') || localStorage.getItem('admin_user') || localStorage.getItem('empleado_user');
    if (raw) {
      try {
        const user = JSON.parse(raw);
        const role = user.Rol || (user.Usuario === 'admin' ? 'admin' : 'empleado');
        if (role === 'admin') {
          document.body.classList.remove('theme-empleado');
          document.body.classList.add('theme-admin');
        } else {
          document.body.classList.remove('theme-admin');
          document.body.classList.add('theme-empleado');
        }
      } catch (e) {
        console.warn('Error al restaurar tema:', e);
      }
    }
  }
}

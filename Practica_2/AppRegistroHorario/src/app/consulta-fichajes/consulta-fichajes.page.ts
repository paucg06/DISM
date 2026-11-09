import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService, Fichaje, Usuario } from '../services/api';
import { Router } from '@angular/router';

@Component({
  selector: 'app-consulta-fichajes',
  templateUrl: './consulta-fichajes.page.html',
  styleUrls: ['./consulta-fichajes.page.scss'],
  standalone: false
})
export class ConsultaFichajesPage implements OnInit {
  usuarioActual: Usuario | null = null;
  fichajes: Fichaje[] = [];
  cargando: boolean = false;

  filtroFechaInicio = '';
  filtroFechaFin = '';

  constructor(
    private api: ApiService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.cargarUsuario();
    this.consultar();
  }

  ionViewWillEnter() {
    if (this.cargarUsuario()) {
      this.consultar();
    }
  }

  cargarUsuario(): boolean {
    const raw = localStorage.getItem('auth_user');
    if (!raw) {
      this.router.navigate(['/login'], { replaceUrl: true });
      return false;
    }
    this.usuarioActual = JSON.parse(raw);
    return true;
  }

  consultar() {
    if (!this.cargarUsuario()) return;
    this.cargando = true;
    this.cdr.detectChanges();

    // Timeout de seguridad máximo de 400 ms para garantizar fluidez absoluta
    const safetyTimeout = setTimeout(() => {
      this.cargando = false;
      this.cdr.detectChanges();
    }, 400);

    this.api.getFichajesUsuario(this.usuarioActual!.IdUsuario, this.filtroFechaInicio, this.filtroFechaFin).subscribe({
      next: (data) => {
        clearTimeout(safetyTimeout);
        this.fichajes = data || [];
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: () => {
        clearTimeout(safetyTimeout);
        this.fichajes = [];
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });
  }

  limpiarFiltros() {
    this.filtroFechaInicio = '';
    this.filtroFechaFin = '';
    this.consultar();
  }

  logout() {
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}

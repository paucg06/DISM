import { Component, OnInit } from '@angular/core';
import { ApiService, Fichaje, Usuario } from '../services/api';
import { Router } from '@angular/router';

interface FichajeConDireccion extends Fichaje {
  direccionPostal?: string;
}

@Component({
  selector: 'app-consulta-fichajes',
  templateUrl: './consulta-fichajes.page.html',
  styleUrls: ['./consulta-fichajes.page.scss'],
  standalone: false
})
export class ConsultaFichajesPage implements OnInit {
  usuarioActual: Usuario | null = null;
  fichajes: FichajeConDireccion[] = [];
  cargando = false;

  filtroFechaInicio = '';
  filtroFechaFin = '';

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  ngOnInit() {
    this.cargarUsuario();
    this.cargarFichajesDeHoy();
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

  cargarFichajesDeHoy() {
    if (!this.usuarioActual) return;
    const pad = (n: number) => String(n).padStart(2, '0');
    const d = new Date();
    const hoyStr = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

    this.filtroFechaInicio = hoyStr;
    this.filtroFechaFin = hoyStr;
    this.consultar();
  }

  consultar() {
    if (!this.cargarUsuario()) return;
    this.cargando = true;

    // Timeout de seguridad de 2 segundos para no bloquear la interfaz
    const safetyTimeout = setTimeout(() => {
      this.cargando = false;
    }, 2000);

    this.api.getFichajesUsuario(this.usuarioActual!.IdUsuario, this.filtroFechaInicio, this.filtroFechaFin).subscribe({
      next: (data) => {
        clearTimeout(safetyTimeout);
        this.fichajes = data || [];
        this.cargando = false;
        this.geocodificarFichajes();
      },
      error: () => {
        clearTimeout(safetyTimeout);
        this.fichajes = [];
        this.cargando = false;
      }
    });
  }

  limpiarFiltros() {
    this.filtroFechaInicio = '';
    this.filtroFechaFin = '';
    this.consultar();
  }

  geocodificarFichajes() {
    for (const f of this.fichajes) {
      if (f.GeolocalizacionLatitud && f.GeolocalizacionLongitud) {
        this.api.getDireccionNominatim(f.GeolocalizacionLatitud, f.GeolocalizacionLongitud).subscribe({
          next: (res) => {
            f.direccionPostal = res.display_name || `Lat: ${f.GeolocalizacionLatitud}, Lon: ${f.GeolocalizacionLongitud}`;
          },
          error: () => {
            f.direccionPostal = `Lat: ${f.GeolocalizacionLatitud}, Lon: ${f.GeolocalizacionLongitud}`;
          }
        });
      }
    }
  }

  logout() {
    localStorage.clear();
    sessionStorage.clear();
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}

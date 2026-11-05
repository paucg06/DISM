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
    const raw = localStorage.getItem('empleado_user');
    if (!raw) {
      this.router.navigate(['/login']);
      return;
    }
    this.usuarioActual = JSON.parse(raw);
    this.cargarFichajesDeHoy();
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
    if (!this.usuarioActual) return;
    this.cargando = true;

    this.api.getFichajesUsuario(this.usuarioActual.IdUsuario, this.filtroFechaInicio, this.filtroFechaFin).subscribe({
      next: (data) => {
        this.fichajes = data;
        this.cargando = false;
        // Obtener la georreferenciación inversa con Nominatim para cada fichaje
        this.geocodificarFichajes();
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  geocodificarFichajes() {
    for (const f of this.fichajes) {
      if (f.GeolocalizacionLatitud && f.GeolocalizacionLongitud) {
        this.api.getDireccionNominatim(f.GeolocalizacionLatitud, f.GeolocalizacionLongitud).subscribe({
          next: (res) => {
            f.direccionPostal = res.display_name || 'Dirección no disponible';
          },
          error: () => {
            f.direccionPostal = `Coordenadas: [${f.GeolocalizacionLatitud}, ${f.GeolocalizacionLongitud}]`;
          }
        });
      }
    }
  }

  limpiarFiltros() {
    this.filtroFechaInicio = '';
    this.filtroFechaFin = '';
    this.consultar();
  }
}

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Usuario {
  IdUsuario: number;
  Nombre: string;
  Usuario: string;
  Rol?: string;
}

export interface Trabajo {
  IdTrabajo: number;
  Nombre: string;
}

export interface Fichaje {
  IdFichaje: number;
  FechaHoraEntrada: string;
  FechaHoraSalida?: string | null;
  HorasTrabajadas?: number | null;
  IdTrabajo: number;
  NombreTrabajo?: string;
  IdUsuario: number;
  NombreUsuario?: string;
  GeolocalizacionLatitud: number;
  GeolocalizacionLongitud: number;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private basePath = 'http://localhost:8080/api/v1/';
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'x-api-key': 'dism-secret-key-2026'
    })
  };

  constructor(private http: HttpClient) {}

  login(usuario: string, clave: string): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.basePath}auth/login`, { usuario, clave }, this.httpOptions);
  }

  getTrabajos(): Observable<Trabajo[]> {
    return this.http.get<Trabajo[]>(`${this.basePath}trabajos`, this.httpOptions);
  }

  getUltimoFichajeActivo(idUsuario: number): Observable<Fichaje | null> {
    return this.http.get<Fichaje | null>(`${this.basePath}fichajes/ultimo-activo/${idUsuario}`, this.httpOptions);
  }

  iniciarFichaje(datos: { IdUsuario: number; IdTrabajo: number; GeolocalizacionLatitud: number; GeolocalizacionLongitud: number }): Observable<Fichaje> {
    return this.http.post<Fichaje>(`${this.basePath}fichajes`, datos, this.httpOptions);
  }

  cerrarFichaje(idFichaje: number): Observable<Fichaje> {
    return this.http.put<Fichaje>(`${this.basePath}fichajes/cerrar/${idFichaje}`, {}, this.httpOptions);
  }

  getFichajesUsuario(idUsuario: number, fechaInicio?: string, fechaFin?: string): Observable<Fichaje[]> {
    let url = `${this.basePath}fichajes?idUsuario=${idUsuario}`;
    if (fechaInicio) url += `&fechaInicio=${fechaInicio}`;
    if (fechaFin) url += `&fechaFin=${fechaFin}`;
    return this.http.get<Fichaje[]>(url, this.httpOptions);
  }

  // Georreferenciación inversa con Nominatim OpenStreetMap
  getDireccionNominatim(lat: number, lon: number): Observable<any> {
    const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&addressdetails=1`;
    return this.http.get(url);
  }
}

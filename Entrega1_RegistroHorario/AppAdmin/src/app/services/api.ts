import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Usuario {
  IdUsuario: number;
  Nombre: string;
  Usuario: string;
  Clave?: string;
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

  // Autenticación
  login(usuario: string, clave: string): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.basePath}auth/login`, { usuario, clave }, this.httpOptions);
  }

  // CRUD Usuarios
  getUsuarios(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(`${this.basePath}usuarios`, this.httpOptions);
  }

  getUsuario(id: number): Observable<Usuario> {
    return this.http.get<Usuario>(`${this.basePath}usuarios/${id}`, this.httpOptions);
  }

  crearUsuario(usuario: Usuario): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.basePath}usuarios`, usuario, this.httpOptions);
  }

  actualizarUsuario(id: number, usuario: Usuario): Observable<Usuario> {
    return this.http.put<Usuario>(`${this.basePath}usuarios/${id}`, usuario, this.httpOptions);
  }

  eliminarUsuario(id: number): Observable<any> {
    return this.http.delete(`${this.basePath}usuarios/${id}`, this.httpOptions);
  }

  // CRUD Trabajos
  getTrabajos(): Observable<Trabajo[]> {
    return this.http.get<Trabajo[]>(`${this.basePath}trabajos`, this.httpOptions);
  }

  getTrabajo(id: number): Observable<Trabajo> {
    return this.http.get<Trabajo>(`${this.basePath}trabajos/${id}`, this.httpOptions);
  }

  crearTrabajo(trabajo: Trabajo): Observable<Trabajo> {
    return this.http.post<Trabajo>(`${this.basePath}trabajos`, trabajo, this.httpOptions);
  }

  actualizarTrabajo(id: number, trabajo: Trabajo): Observable<Trabajo> {
    return this.http.put<Trabajo>(`${this.basePath}trabajos/${id}`, trabajo, this.httpOptions);
  }

  eliminarTrabajo(id: number): Observable<any> {
    return this.http.delete(`${this.basePath}trabajos/${id}`, this.httpOptions);
  }

  // Fichajes
  getFichajes(filtros?: { idUsuario?: number; fechaInicio?: string; fechaFin?: string }): Observable<Fichaje[]> {
    let url = `${this.basePath}fichajes?`;
    if (filtros) {
      if (filtros.idUsuario) url += `idUsuario=${filtros.idUsuario}&`;
      if (filtros.fechaInicio) url += `fechaInicio=${filtros.fechaInicio}&`;
      if (filtros.fechaFin) url += `fechaFin=${filtros.fechaFin}&`;
    }
    return this.http.get<Fichaje[]>(url, this.httpOptions);
  }
}

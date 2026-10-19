import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Usuario } from '../models/usuario';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // API Path
  basePath = 'http://localhost:3000/';

  constructor(private http: HttpClient) { }

  // Opciones Http
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  // Manejador de errores API
  handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error("Ha ocurrido un error:", error.error.message);
    } else {
      console.error(
        `Código Error: ${error.status}, ` +
        `Body: ${error.error}`
      );
    }
    return throwError(() => new Error('Ha sucedido un problema, inténtalo más tarde'));
  }

  createItem(item: Usuario): Observable<Usuario> {
    return this.http.post<Usuario>(this.basePath + 'usuarios/', JSON.stringify(item), this.httpOptions)
      .pipe(retry(2), catchError(this.handleError));
  }

  getItem(id: number): Observable<Usuario> {
    return this.http.get<Usuario>(this.basePath + 'usuarios/' + id)
      .pipe(retry(2), catchError(this.handleError));
  }

  getList(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(this.basePath + 'usuarios/')
      .pipe(retry(2), catchError(this.handleError));
  }

  updateItem(item: Usuario): Observable<Usuario> {
    console.log("UPDATE: " + JSON.stringify(item));
    return this.http.put<Usuario>(this.basePath + 'usuarios/' + item.id, JSON.stringify(item), this.httpOptions)
      .pipe(retry(2), catchError(this.handleError));
  }

  deleteItem(id: number): Observable<Usuario> {
    return this.http.delete<Usuario>(this.basePath + 'usuarios/' + id, this.httpOptions)
      .pipe(retry(2), catchError(this.handleError));
  }
}

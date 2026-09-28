# 📚 Resumen de Prácticas DISM (Desarrollo de Interfaces y Servicios Móviles)

Este documento recopila de forma estructurada, directa y comentada los ejercicios realizados desde la **Práctica 0** hasta la **Práctica 7**, listo para repasar y defender ante el profesorado.

---

## 🗂️ Estructura General del Espacio de Trabajo

```text
📁 workspace/
│
├── 📁 DISM0/                # Ejercicio 0: Verificación del entorno y plantilla base Tabs
│   └── 📁 src/
│
├── 📁 DISM1/                # Ejercicio 1: Navegación TABS, Botones, Listas, Cards y Toggles
│   └── 📁 src/app/
│       ├── 📁 tabs/         # Barra de navegación principal (tabs.page.html / tabs.page.ts)
│       ├── 📁 tab1/         # Tipos de botones (ion-button)
│       ├── 📁 tab2/         # Listas estáticas y dinámicas (@for)
│       ├── 📁 tab3/         # Tarjeta multimedia con imagen de gato (ion-card)
│       └── 📁 formulario/   # Interruptores y estados (ion-toggle)
│
├── 📁 DISM2/                # Ejercicio 2: Menú Lateral (Side Menu) y Navegación
│   └── 📁 src/app/
│       ├── app.component.*  # Menú con ion-split-pane y ion-menu
│       ├── 📁 home/         # Página Inicio con navegación a Créditos
│       └── 📁 credits/      # Página Créditos con botones de retorno a Inicio
│
├── 📁 DISM3/                # Ejercicio 3: Inyección de Dependencias, Servicios y API REST
│   └── 📁 src/
│       ├── main.ts          # Configuración global del cliente HTTP (provideHttpClient)
│       └── 📁 app/
│           ├── 📁 services/ # Servicio http.ts para consumir la API de RandomUser
│           └── 📁 home/     # Vista con listado dinámico, avatar y botón de carga
│
├── 📁 DISM4/                # Ejercicio 4: Creación de Fake API REST con JSON-Server
│   └── db.json              # Base de datos simulada en formato JSON
│
├── 📁 DISM5/                # Ejercicio 5: Aplicación CRUD completa consumiendo la Fake REST API
│   └── 📁 src/app/
│       ├── 📁 models/       # Modelo de datos Usuario (usuario.ts)
│       ├── 📁 services/     # Servicio ApiService con métodos GET, POST, PUT, DELETE (api.ts)
│       ├── 📁 home/         # Listado de usuarios con botones editar y borrar
│       ├── 📁 nuevo/        # Formulario de creación con ngModel (Nombre, Edad, Email) y POST
│       └── 📁 editar/       # Formulario de edición con ngModel y PUT
│
├── 📁 DISM6/                # Ejercicio 6: Geolocalización y Georreferenciación Inversa
│   └── 📁 src/app/
│       └── 📁 home/         # Obtención de coordenadas GPS y llamada a API Nominatim
│
└── 📁 DISM7/                # Ejercicio 7: Mapas Interactivos con Leaflet y OpenStreetMap
    └── 📁 src/app/
        └── 📁 home/         # Renderizado de mapa, capas de teselas y marcadores
```

---

## 🚀 Ejercicio 0: Instalación y Comprobación del Entorno (`DISM0`)

### 🎯 Objetivo
Verificar la correcta instalación de **Node.js LTS**, el gestor **NPM** y el **CLI de Ionic**, creando una aplicación base con plantilla `tabs` y arquitectura Standalone de Angular.

### 🛠️ Comandos clave
```bash
# 1. Comprobación de versiones
node -v
npm -v
ionic -v

# 2. Creación del proyecto base
ionic start DISM0 tabs --type=angular-standalone --no-interactive

# 3. Lanzar servidor de desarrollo
cd DISM0
ionic serve
```

---

## 📱 Ejercicio 1: Aplicación TABS y Componentes de Interfaz (`DISM1`)

### 🎯 Objetivo
Personalizar la navegación por pestañas (`ion-tabs`), añadir una nueva página (`formulario`), y dominar los componentes visuales esenciales de Ionic: botones, listas, tarjetas y selectores toggle.

---

### 1. Barra de Pestañas y Rutas
📍 **Archivo:** `DISM1/src/app/tabs/tabs.page.html`
```html
<!-- Barra inferior de navegación que agrupa los accesos a cada vista -->
<ion-tabs>
  <ion-tab-bar slot="bottom">
    <ion-tab-button tab="tab1" href="/tabs/tab1">
      <ion-icon aria-hidden="true" name="triangle"></ion-icon>
      <ion-label>Inicio</ion-label>
    </ion-tab-button>

    <!-- Pestaña adicional creada mediante 'ionic generate page formulario' -->
    <ion-tab-button tab="formulario" href="/tabs/formulario">
      <ion-icon aria-hidden="true" name="list"></ion-icon>
      <ion-label>Formulario</ion-label>
    </ion-tab-button>

    <ion-tab-button tab="tab2" href="/tabs/tab2">
      <ion-icon aria-hidden="true" name="ellipse"></ion-icon>
      <ion-label>Acerca de</ion-label>
    </ion-tab-button>

    <ion-tab-button tab="tab3" href="/tabs/tab3">
      <ion-icon aria-hidden="true" name="square"></ion-icon>
      <ion-label>Contacto</ion-label>
    </ion-tab-button>
  </ion-tab-bar>
</ion-tabs>
```

📍 **Archivo:** `DISM1/src/app/tabs/tabs.page.ts`
```typescript
import { Component, EnvironmentInjector, inject } from '@angular/core';
import { IonTabs, IonTabBar, IonTabButton, IonIcon, IonLabel } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { triangle, ellipse, square, list } from 'ionicons/icons';

@Component({
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  imports: [IonTabs, IonTabBar, IonTabButton, IonIcon, IonLabel],
})
export class TabsPage {
  constructor() {
    // Registra los iconos vectoriales utilizados en la barra de navegación
    addIcons({ triangle, ellipse, square, list });
  }
}
```

---

### 2. Tab 1: Variantes de Botones (`ion-button`)
📍 **Archivo:** `DISM1/src/app/tab1/tab1.page.html`
```html
<ion-content [fullscreen]="true">
  <!-- Botones básicos y estados -->
  <ion-button>Default</ion-button>
  <ion-button [disabled]="true">Disabled</ion-button>

  <!-- Botones de ancho completo -->
  <ion-button expand="block">Block</ion-button>
  <ion-button expand="full">Full</ion-button>

  <!-- Formas y estilos de relleno -->
  <ion-button shape="round">Round</ion-button>
  <ion-button fill="outline">Outline</ion-button>
  <ion-button fill="clear">Clear</ion-button>

  <!-- Botones con iconos -->
  <ion-button>
    <ion-icon slot="start" name="star"></ion-icon>
    Left Icon
  </ion-button>

  <!-- Colores temáticos de Ionic -->
  <ion-button color="primary">Primary</ion-button>
  <ion-button color="secondary">Secondary</ion-button>
  <ion-button color="danger">Danger</ion-button>
</ion-content>
```

---

### 3. Tab 2: Listas Estáticas y Dinámicas (`ion-list`)
📍 **Archivo:** `DISM1/src/app/tab2/tab2.page.ts`
```typescript
import { Component } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonLabel } from '@ionic/angular';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  imports: [IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonLabel],
})
export class Tab2Page {
  // Array de objetos para generar la lista dinámica
  lista = [
    { name: 'Lechuga' },
    { name: 'Tomate' },
    { name: 'Alcachofa' }
  ];
}
```

📍 **Archivo:** `DISM1/src/app/tab2/tab2.page.html`
```html
<ion-content [fullscreen]="true">
  <h2>Lista Estática</h2>
  <ion-list>
    <ion-item><ion-label>Sandía</ion-label></ion-item>
    <ion-item><ion-label>Naranja</ion-label></ion-item>
    <ion-item><ion-label>Fresa</ion-label></ion-item>
  </ion-list>

  <h2>Lista Dinámica</h2>
  <ion-list>
    <!-- Renderizado reactivo con la directiva @for moderna de Angular -->
    @for (item of lista; track $index) {
      <ion-item>
        <h5>{{ item.name }}</h5>
      </ion-item>
    }
  </ion-list>
</ion-content>
```

---

### 4. Tab 3: Tarjeta Multimedia (`ion-card`)
📍 **Archivo:** `DISM1/src/app/tab3/tab3.page.html`
```html
<ion-content [fullscreen]="true">
  <!-- Contenedor de tarjeta estándar -->
  <ion-card>
    <!-- Imagen del gato ubicada en los recursos locales assets/img/ -->
    <img src="../../assets/img/img.jpg" alt="Foto gato" />
    <ion-card-header>
      <ion-card-subtitle>minim dicant sensibus</ion-card-subtitle>
      <ion-card-title>Melius fabella</ion-card-title>
    </ion-card-header>
    <ion-card-content>
      Mei eu mollis albucius, ex nisl contentiones vix. Duo persius volutpat at, cu iuvaret epicuri mei.
    </ion-card-content>
  </ion-card>
</ion-content>
```

---

### 5. Formulario: Interruptores (`ion-toggle`)
📍 **Archivo:** `DISM1/src/app/formulario/formulario.page.html`
```html
<ion-content [fullscreen]="true">
  <!-- Toggles independientes con diferentes estados -->
  <ion-toggle>Default Toggle</ion-toggle>
  <ion-toggle [checked]="true">Checked Toggle</ion-toggle>
  <ion-toggle [disabled]="true">Disabled Toggle</ion-toggle>

  <!-- Toggles agrupados en una lista para formularios de ajustes -->
  <ion-list>
    <ion-item>
      <ion-toggle>Receive Push Notifications</ion-toggle>
    </ion-item>
    <ion-item>
      <ion-toggle>Receive Emails</ion-toggle>
    </ion-item>
  </ion-list>
</ion-content>
```

---

## 🧭 Ejercicio 2: Menú Lateral (Side Menu) y Navegación (`DISM2`)

### 🎯 Objetivo
Construir una navegación lateral tipo hamburguesa/split pane desde una plantilla en blanco (`blank`) y permitir transiciones de ida y vuelta entre la página principal (**Home**) y la página secundaria (**Créditos**) mediante navegación declarativa y programática.

---

### 1. Plantilla Principal con Menú Desplegable
📍 **Archivo:** `DISM2/src/app/app.component.html`
```html
<ion-app>
  <!-- ion-split-pane: Muestra menú fijo en pantallas grandes y colapsable en móviles -->
  <ion-split-pane contentId="main-content">
    
    <!-- Definición del menú lateral -->
    <ion-menu contentId="main-content">
      <ion-header>
        <ion-toolbar>
          <ion-title>Menú</ion-title>
        </ion-toolbar>
      </ion-header>
      <ion-content>
        <ion-list>
          <ion-menu-toggle auto-hide="false">
            <!-- Enlaces directos a las rutas principales -->
            <ion-item [routerDirection]="'root'" [routerLink]="'/home'">
              <ion-icon slot="start" [name]="'home'"></ion-icon>
              <ion-label>Inicio</ion-label>
            </ion-item>
            <ion-item [routerDirection]="'root'" [routerLink]="'/credits'">
              <ion-icon slot="start" [name]="'help-circle'"></ion-icon>
              <ion-label>Créditos</ion-label>
            </ion-item>
          </ion-menu-toggle>
        </ion-list>
      </ion-content>
    </ion-menu>

    <!-- Contenedor donde se cargan las páginas activas -->
    <ion-router-outlet id="main-content"></ion-router-outlet>
  </ion-split-pane>
</ion-app>
```

📍 **Archivo:** `DISM2/src/app/app.component.ts`
```typescript
import { Component } from '@angular/core';
import { IonIcon, IonApp, IonRouterOutlet, IonItem, IonSplitPane, IonMenu,
  IonHeader, IonToolbar, IonTitle, IonLabel, IonContent, IonList, IonMenuToggle } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { helpCircle, home } from 'ionicons/icons';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  imports: [RouterModule, IonItem, IonApp, IonRouterOutlet, IonSplitPane, IonMenu, 
            IonHeader, IonToolbar, IonTitle, IonLabel, IonContent, IonList, IonMenuToggle, IonIcon],
})
export class AppComponent {
  constructor() {
    // Registra los iconos usados en las opciones del menú
    addIcons({ helpCircle, home });
  }
}
```

---

### 2. Navegación en Home y Créditos (Ida y Vuelta)
📍 **Archivo:** `DISM2/src/app/home/home.page.html`
```html
<ion-header [translucent]="true">
  <ion-toolbar>
    <ion-title>Home</ion-title>
    <!-- Botón hamburguesa para abrir el menú lateral -->
    <ion-buttons slot="start">
      <ion-menu-button></ion-menu-button>
    </ion-buttons>
  </ion-toolbar>
</ion-header>

<ion-content [fullscreen]="true">
  <!-- Método 1: Navegación declarativa con routerLink -->
  <ion-button [routerLink]="['/credits']" color="primary" expand="block">
    Créditos
  </ion-button>

  <!-- Método 2: Navegación programática mediante evento click y TypeScript -->
  <ion-button (click)="mostrarPagina()" color="secondary" expand="block">
    Créditos 2
  </ion-button>
</ion-content>
```

📍 **Archivo:** `DISM2/src/app/home/home.page.ts`
```typescript
import { Component } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonMenuButton, IonButton } from '@ionic/angular';
import { RouterModule, Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  imports: [RouterModule, IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonMenuButton, IonButton],
})
export class HomePage {
  // Inyección del servicio Router de Angular
  constructor(private router: Router) {}

  // Redirección por código a la ruta /credits
  mostrarPagina() {
    this.router.navigate(['/credits']);
  }
}
```

---

## 🌐 Ejercicio 3: Servicios y Conexión con API REST (`DISM3`)

### 🎯 Objetivo
Aprender la arquitectura de **servicios** (proveedores de datos) en Angular/Ionic para desacoplar la lógica de red de las vistas, consumiendo una API REST pública (`https://randomuser.me/api/?results=25`) y mostrando avatares, nombres y emails dinámicamente.

---

### 1. Registro del Proveedor HTTP Global
📍 **Archivo:** `DISM3/src/main.ts`
```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { RouteReuseStrategy, provideRouter, withComponentInputBinding, withPreloading, PreloadAllModules } from '@angular/router';
import { IonicRouteStrategy, provideIonicAngular } from '@ionic/angular';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app/app.routes';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, {
  providers: [
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    provideIonicAngular(),
    provideRouter(routes, withPreloading(PreloadAllModules), withComponentInputBinding()),
    provideHttpClient(), // Habilita la inyección de HttpClient en toda la app
  ],
});
```

---

### 2. Creación del Servicio HTTP
📍 **Archivo:** `DISM3/src/app/services/http.ts`
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root' // Servicio disponible globalmente como Singleton
})
export class HttpService {
  // Se inyecta el cliente HTTP oficial de Angular
  constructor(public http: HttpClient) { }

  // Realiza una petición GET al endpoint remoto solicitando 25 usuarios
  loadUsers() {
    return this.http.get('https://randomuser.me/api/?results=25');
  }
}
```

---

### 3. Vista de Usuarios con Avatar y Estado Vacío
📍 **Archivo:** `DISM3/src/app/home/home.page.html`
```html
<ion-header [translucent]="true">
  <ion-toolbar>
    <ion-title>Usuarios</ion-title>
  </ion-toolbar>
</ion-header>

<ion-content [fullscreen]="true">
  <ion-list>
    <!-- Recorrido dinámico del array 'usuarios' con identificador único por email -->
    @for (usuario of usuarios; track usuario.email) {
      <ion-item>
        <ion-avatar slot="start">
          <ion-img [src]="usuario.picture.medium"></ion-img>
        </ion-avatar>
        <ion-label>
          <h2>{{ usuario.name.first }}</h2>
          <p>{{ usuario.email }}</p>
        </ion-label>
      </ion-item>
    } @empty {
      <!-- Se muestra automáticamente si el array está vacío antes de pulsar el botón -->
      <ion-item>
        <ion-label>No hay usuarios</ion-label>
      </ion-item>
    }
  </ion-list>

  <!-- Botón de acción para desencadenar la llamada HTTP -->
  <ion-button expand="block" (click)="cargarUsuarios()">
    Cargar Usuarios
  </ion-button>
</ion-content>
```

---

### 4. Controlador y Manejo Asíncrono
📍 **Archivo:** `DISM3/src/app/home/home.page.ts`
```typescript
import { Component } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonList,
  IonItem, IonAvatar, IonImg, IonLabel, IonButton } from '@ionic/angular';
import { HttpService } from '../services/http';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonButton, IonLabel, IonImg, IonAvatar, IonItem, IonList, IonHeader, IonToolbar, IonTitle, IonContent],
})
export class HomePage {
  usuarios: any[] = []; // Almacén de los datos obtenidos de la API

  // Inyección del servicio creado previamente
  constructor(private http: HttpService) {}

  // Función asíncrona que convierte el Observable en Promesa y actualiza la lista
  async cargarUsuarios() {
    try {
      const res: any = await firstValueFrom(this.http.loadUsers());
      this.usuarios = res.results; // Se extrae la lista de resultados de la respuesta
    } catch (error) {
      console.error('Error al obtener los usuarios:', error);
    }
  }
}
```

---

## 🛠️ Ejercicio 4: Creación de una Fake API REST con JSON-Server (`DISM4`)

### 🎯 Objetivo
Configurar un servidor backend simulado (*Mock/Fake API REST*) para desarrollo móvil cuando aún no se dispone del backend real, permitiendo operaciones completas CRUD (GET, POST, PUT, DELETE) basadas en un archivo JSON.

---

### 1. Instalación y Base de Datos JSON
```bash
# Instalación global del servidor mock
npm install -g json-server
```

📍 **Archivo:** `DISM4/db.json`
```json
{
  "usuarios": [
    { "id": "1", "nombre": "Sergio", "email": "sergio@ua.es", "edad": "21" },
    { "id": "2", "nombre": "Estela", "email": "estela@ua.es", "edad": "19" },
    { "id": "3", "nombre": "Susana", "email": "susana@ua.es", "edad": "27" },
    { "id": "4", "nombre": "Hugo", "email": "hugo@ua.es", "edad": "18" }
  ]
}
```

---

### 2. Ejecución y Endpoints Disponibles
```bash
# Desde la carpeta DISM4
json-server db.json
```
- **URL Base:** `http://localhost:3000`
- **Endpoint:** `http://localhost:3000/usuarios` (Soporta GET, POST, PUT, DELETE).

---

## ⚡ Ejercicio 5: Aplicación CRUD Completa consumiendo Fake REST API (`DISM5`)

### 🎯 Objetivo
Desarrollar una aplicación móvil completa que realice el ciclo completo de operaciones **CRUD** (*Create, Read, Update, Delete*) conectándose al backend `DISM4` a través de un servicio Angular con manejo de errores y operadores RxJS (`retry`, `catchError`).

---

### 1. Modelo de Datos
📍 **Archivo:** `DISM5/src/app/models/usuario.ts`
```typescript
// Define la estructura tipada de la entidad Usuario
export class Usuario {
  id: number = 0;
  nombre: string = "";
  email: string = "";
  edad: string = "";
}
```

---

### 2. Servicio API con Operaciones CRUD y Manejo de Errores
📍 **Archivo:** `DISM5/src/app/services/api.ts`
```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Usuario } from '../models/usuario';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  basePath = 'http://localhost:3000/'; // URL base del json-server

  constructor(private http: HttpClient) { }

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json' // Cabecera estándar para enviar JSON
    })
  };

  // Centralizador de captura y registro de errores de red o servidor
  handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error("Ha ocurrido un error:", error.error.message);
    } else {
      console.error(`Código Error: ${error.status}, Body: ${error.error}`);
    }
    return throwError(() => new Error('Ha sucedido un problema, inténtalo más tarde'));
  }

  // CREATE (POST)
  createItem(item: Usuario): Observable<Usuario> {
    return this.http.post<Usuario>(this.basePath + 'usuarios/', JSON.stringify(item), this.httpOptions)
      .pipe(retry(2), catchError(this.handleError));
  }

  // READ (GET por ID)
  getItem(id: number): Observable<Usuario> {
    return this.http.get<Usuario>(this.basePath + 'usuarios/' + id)
      .pipe(retry(2), catchError(this.handleError));
  }

  // READ ALL (GET Lista)
  getList(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(this.basePath + 'usuarios/')
      .pipe(retry(2), catchError(this.handleError));
  }

  // UPDATE (PUT)
  updateItem(item: Usuario): Observable<Usuario> {
    return this.http.put<Usuario>(this.basePath + 'usuarios/' + item.id, JSON.stringify(item), this.httpOptions)
      .pipe(retry(2), catchError(this.handleError));
  }

  // DELETE (DELETE)
  deleteItem(id: number): Observable<Usuario> {
    return this.http.delete<Usuario>(this.basePath + 'usuarios/' + id, this.httpOptions)
      .pipe(retry(2), catchError(this.handleError));
  }
}
```

---

### 3. Vista Principal: Listado, Botones de Edición, Borrado y Nuevo
📍 **Archivo:** `DISM5/src/app/home/home.page.html`
```html
<ion-header [translucent]="true">
  <ion-toolbar>
    <ion-title>Listado Usuarios</ion-title>
  </ion-toolbar>
</ion-header>

<ion-content class="ion-padding">
  <ion-list>
    <!-- Recorrido de los usuarios recibidos de la API -->
    @for (item of UsuarioData; track item.id) {
      <ion-item>
        <ion-label>
          <h2>Id: {{ item.id }}</h2>
          <h2>Nombre: {{ item.nombre }}</h2>
          <p>Email: {{ item.email }}</p>
          <p>Edad: {{ item.edad }}</p>
        </ion-label>
        
        <!-- Botón para editar: envía el usuario seleccionado como estado -->
        <ion-button (click)="editUsuario(item)" color="warning" size="small">
          <ion-icon name="create"></ion-icon>
        </ion-button>
        
        <!-- Botón para eliminar el usuario -->
        <ion-button (click)="deleteUsuario(item)" color="danger" size="small">
          <ion-icon name="trash"></ion-icon>
        </ion-button>
      </ion-item>
    } @empty {
      <ion-item>
        <ion-label>No hay usuarios disponibles</ion-label>
      </ion-item>
    }
  </ion-list>

  <!-- Botón para navegar a la pantalla de creación -->
  <ion-button [routerLink]="['/nuevo']" expand="block">
    Nuevo Usuario
  </ion-button>
</ion-content>
```

📍 **Archivo:** `DISM5/src/app/home/home.page.ts`
```typescript
import { Component } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonLabel, IonButton, IonIcon } from '@ionic/angular';
import { Usuario } from '../models/usuario';
import { ApiService } from '../services/api';
import { NavController } from '@ionic/angular';
import { RouterLink } from '@angular/router';
import { addIcons } from 'ionicons';
import { create, trash } from 'ionicons/icons';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonIcon, IonButton, IonLabel, IonItem, IonList, IonHeader, IonToolbar, IonTitle, IonContent, RouterLink],
})
export class HomePage {
  UsuarioData: Usuario[] = [];

  constructor(
    public apiService: ApiService,
    private nav: NavController
  ) {
    addIcons({ create, trash });
  }

  ionViewWillEnter() {
    this.getAllUsuarios();
  }

  getAllUsuarios() {
    this.apiService.getList().subscribe({
      next: (response: Usuario[]) => { this.UsuarioData = response; },
      error: (err) => { console.error('Error al obtener usuarios:', err); }
    });
  }

  deleteUsuario(item: Usuario) {
    this.apiService.deleteItem(item.id).subscribe({
      next: () => { this.getAllUsuarios(); },
      error: (err) => { console.error('Error al eliminar usuario:', err); }
    });
  }

  // Navega a la vista de edición pasando el objeto en el state de navegación
  editUsuario(item: Usuario) {
    this.nav.navigateForward('editar', { state: { item } });
  }
}
```

---

### 4. Vista y Lógica de Edición (`editar`)
📍 **Archivo:** `DISM5/src/app/editar/editar.page.html`
```html
<ion-header [translucent]="true">
  <ion-toolbar>
    <ion-title>Editar</ion-title>
  </ion-toolbar>
</ion-header>

<ion-content class="ion-padding">
  <!-- Enlace bidireccional de datos con [(ngModel)] -->
  <ion-item>
    <ion-label>Id:</ion-label>
    <ion-input [(ngModel)]="UsuarioData.id" placeholder="Id"></ion-input>
  </ion-item>
  <ion-item>
    <ion-label>Nombre:</ion-label>
    <ion-input [(ngModel)]="UsuarioData.nombre" placeholder="Nombre"></ion-input>
  </ion-item>
  <ion-item>
    <ion-label>Edad:</ion-label>
    <ion-input [(ngModel)]="UsuarioData.edad" placeholder="Edad"></ion-input>
  </ion-item>
  <ion-item>
    <ion-label>Email:</ion-label>
    <ion-input [(ngModel)]="UsuarioData.email" placeholder="Email"></ion-input>
  </ion-item>

  <ion-button (click)="update()" color="success" expand="block">Actualizar</ion-button>
  <ion-button [routerLink]="['/home']" color="warning" expand="block">Cancelar</ion-button>
</ion-content>
```

📍 **Archivo:** `DISM5/src/app/editar/editar.page.ts`
```typescript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar, IonItem, IonLabel, IonButton, IonInput } from '@ionic/angular';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Usuario } from '../models/usuario';
import { ApiService } from '../services/api';
import { addIcons } from 'ionicons';
import { create, trash } from 'ionicons/icons';

@Component({
  selector: 'app-editar',
  templateUrl: './editar.page.html',
  styleUrls: ['./editar.page.scss'],
  imports: [IonButton, IonLabel, IonItem, IonContent, IonHeader, IonTitle, IonToolbar, CommonModule, FormsModule, RouterLink, IonInput]
})
export class EditarPage implements OnInit {
  id: number = 0;
  UsuarioData: Usuario = { id: 0, nombre: '', edad: '', email: '' };

  constructor(
    public activatedRoute: ActivatedRoute,
    public router: Router,
    public apiService: ApiService
  ) {
    addIcons({ create, trash });
  }

  // Recupera los datos pasados en el state de navegación
  ngOnInit() {
    const navData = history.state as { item: Usuario };
    if (navData && navData.item) {
      this.UsuarioData = navData.item;
    }
  }

  // Envía la petición PUT a la Fake API y regresa a home
  update() {
    this.apiService.updateItem(this.UsuarioData).subscribe({
      next: () => { this.router.navigate(['/home']); },
      error: (err) => { console.error('Error al actualizar usuario:', err); }
    });
  }
}
```

---

### 5. Vista y Lógica de Creación (`nuevo`)
📍 **Archivo:** `DISM5/src/app/nuevo/nuevo.page.html`
```html
<ion-header [translucent]="true">
  <ion-toolbar>
    <ion-title>Nuevo</ion-title>
  </ion-toolbar>
</ion-header>

<ion-content class="ion-padding">
  <ion-item>
    <ion-label>Nombre:</ion-label>
    <ion-input [(ngModel)]="UsuarioData.nombre" placeholder="Nombre"></ion-input>
  </ion-item>

  <ion-item>
    <ion-label>Edad:</ion-label>
    <ion-input [(ngModel)]="UsuarioData.edad" placeholder="Edad"></ion-input>
  </ion-item>

  <ion-item>
    <ion-label>Email:</ion-label>
    <ion-input [(ngModel)]="UsuarioData.email" placeholder="Email"></ion-input>
  </ion-item>

  <ion-button (click)="newUsuario()" color="success" expand="block">Añadir</ion-button>
  <ion-button [routerLink]="['/home']" color="warning" expand="block">Cancelar</ion-button>
</ion-content>
```

📍 **Archivo:** `DISM5/src/app/nuevo/nuevo.page.ts`
```typescript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar, IonItem, IonLabel, IonButton, IonInput } from '@ionic/angular';
import { Usuario } from '../models/usuario';
import { ApiService } from '../services/api';
import { ActivatedRoute, Router } from '@angular/router';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-nuevo',
  templateUrl: './nuevo.page.html',
  styleUrls: ['./nuevo.page.scss'],
  imports: [IonButton, IonLabel, IonItem, IonContent, IonHeader, IonTitle, IonToolbar, CommonModule, FormsModule, RouterLink, IonInput]
})
export class NuevoPage implements OnInit {
  UsuarioData: Usuario = {
    id: 0,
    nombre: '',
    edad: '',
    email: ''
  };

  constructor(
    public activatedRoute: ActivatedRoute,
    public router: Router,
    public apiService: ApiService
  ) {}

  ngOnInit() {
    // Inicialización si necesitas lógica extra
  }

  // Envía la petición POST a la Fake API para registrar un nuevo usuario y regresa a home
  newUsuario() {
    this.apiService.createItem(this.UsuarioData).subscribe({
      next: () => {
        this.router.navigate(['/home']);
      },
      error: (err) => {
        console.error('Error al crear usuario:', err);
      }
    });
  }
}
```

---

## 📍 Ejercicio 6: Geolocalización y Georreferenciación Inversa (`DISM6`)

### 🎯 Objetivo
Acceder a las funciones nativas del dispositivo mediante el plugin `@capacitor/geolocation` para obtener las coordenadas GPS (latitud y longitud) del usuario en tiempo real y traducirlas a una dirección postal humana (*Georreferenciación inversa*) mediante la API pública de **OpenStreetMap (Nominatim)**.

---

### 1. Instalación de Capacitor Geolocation
```bash
# Dentro de la carpeta DISM6
npm install @capacitor/geolocation
```

---

### 2. Configuración Global de HttpClient
📍 **Archivo:** `DISM6/src/main.ts`
```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { RouteReuseStrategy, provideRouter, withPreloading, PreloadAllModules } from '@angular/router';
import { IonicRouteStrategy, provideIonicAngular } from '@ionic/angular';
import { routes } from './app/app.routes';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';

bootstrapApplication(AppComponent, {
  providers: [
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    provideIonicAngular(), provideHttpClient(), // Habilita peticiones HTTP para consultar Nominatim
    provideRouter(routes, withPreloading(PreloadAllModules)),
  ],
});
```

---

### 3. Lógica: Coordenadas GPS y Llamada a Nominatim
📍 **Archivo:** `DISM6/src/app/home/home.page.ts`
```typescript
import { Component } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonList,
  IonLabel, IonItem, IonBadge, IonListHeader } from '@ionic/angular';
import { Geolocation } from '@capacitor/geolocation';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonLabel, IonButton, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonListHeader, IonItem, IonBadge],
})
export class HomePage {
  latitud: any;
  longitud: any;
  direccionGeorreferenciada: any;
  urlNominatim: any;

  constructor(public http: HttpClient) {}

  async locate() {
    // 1. Obtener coordenadas del GPS / navegador mediante Capacitor
    const coordinates = await Geolocation.getCurrentPosition();
    this.latitud = coordinates.coords.latitude;
    this.longitud = coordinates.coords.longitude;
    console.log('Current position:', coordinates);

    // 2. Consulta a la API Nominatim de OpenStreetMap para geocodificación inversa
    this.urlNominatim =
      'https://nominatim.openstreetmap.org/reverse?format=json&lat=' +
      this.latitud +
      '&lon=' +
      this.longitud +
      '&addressdetails=1';

    this.http.get(this.urlNominatim).subscribe((data: any) => {
      this.direccionGeorreferenciada = data.display_name; // Dirección completa en formato texto
      console.log('Address Data:', this.direccionGeorreferenciada);
    });
  }
}
```

---

### 4. Vista de Geolocalización
📍 **Archivo:** `DISM6/src/app/home/home.page.html`
```html
<ion-header [translucent]="true">
  <ion-toolbar>
    <ion-title>Ionic Geolocalización - Georreferenciación</ion-title>
  </ion-toolbar>
</ion-header>

<ion-content [fullscreen]="true">
  <div class="ion-padding">
    <!-- Botón que activa la lectura de coordenadas y geocodificación -->
    <ion-button (click)="locate()" expand="block">
      Obtener Geolocalización-Georreferenciación
    </ion-button>

    <!-- Listado con badges para mostrar las coordenadas y dirección -->
    <ion-list>
      <ion-list-header>
        <ion-label>Coordenadas de Localización</ion-label>
      </ion-list-header>
      
      <ion-item>
        <ion-label>Latitud</ion-label>
        <ion-badge color="danger" slot="end">{{ latitud }}</ion-badge>
      </ion-item>
      
      <ion-item>
        <ion-label>Longitud</ion-label>
        <ion-badge color="danger" slot="end">{{ longitud }}</ion-badge>
      </ion-item>
      
      <ion-item>
        <ion-label>Dirección</ion-label>
        <ion-badge color="warning" slot="end">
          {{ direccionGeorreferenciada }}
        </ion-badge>
      </ion-item>
    </ion-list>
  </div>
</ion-content>
```

---

## 🗺️ Ejercicio 7: Mapas Interactivos con Leaflet (`DISM7`)

### 🎯 Objetivo
Integrar la biblioteca cartográfica de código abierto **Leaflet** en una aplicación Ionic/Angular, cargando la capa de teselas de **OpenStreetMap** y posicionando marcadores interactivos con popups informativos en coordenadas concretas (Alicante y Barcelona).

---

### 1. Instalación de Dependencias
```bash
# Dentro de la carpeta DISM7
npm install leaflet --save
npm i --save-dev @types/leaflet
```

---

### 2. Estilos Globales y Copia de Iconos en `angular.json`
📍 **Archivo:** `DISM7/src/global.scss`
```scss
// Importa las reglas CSS necesarias para renderizar mapas, controles y popups
@import "leaflet/dist/leaflet.css";
```

📍 **Archivo:** `DISM7/angular.json` *(sección `architect.build.options.assets`)*
```json
"assets": [
  "src/assets",
  {
    "glob": "**/*",
    "input": "node_modules/leaflet/dist/images/",
    "output": "./assets/"
  }
]
```

---

### 3. Estilos del Contenedor del Mapa
📍 **Archivo:** `DISM7/src/app/home/home.page.scss`
```scss
// El contenedor debe tener tamaño explícito (100%) para que Leaflet renderice el mapa
#mapId {
  width: 100%;
  height: 100%;
}
```

---

### 4. Vista del Mapa
📍 **Archivo:** `DISM7/src/app/home/home.page.html`
```html
<ion-header [translucent]="true">
  <ion-toolbar color="primary">
    <ion-title>Ionic Mapas con Leaflet</ion-title>
  </ion-toolbar>
</ion-header>

<ion-content>
  <!-- Contenedor donde Leaflet inyecta el lienzo del mapa -->
  <div id="mapId"></div>
</ion-content>
```

---

### 5. Lógica: Inicialización del Mapa, Capa y Marcadores
📍 **Archivo:** `DISM7/src/app/home/home.page.ts`
```typescript
import { Component } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/angular';
import * as Leaflet from 'leaflet';
import { icon, Marker } from 'leaflet';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonHeader, IonToolbar, IonTitle, IonContent],
})
export class HomePage {
  map?: Leaflet.Map;

  constructor() {}

  // ionViewDidEnter: Se ejecuta cuando la vista ya está visible en el DOM (indispensable para Leaflet)
  ionViewDidEnter() {
    this.leafletMap();
  }

  leafletMap() {
    // 1. Configurar los iconos estándar de Leaflet desde assets
    const iconRetinaUrl = 'assets/marker-icon-2x.png';
    const iconUrl = 'assets/marker-icon.png';
    const shadowUrl = 'assets/marker-shadow.png';
    const iconDefault = icon({
      iconRetinaUrl,
      iconUrl,
      shadowUrl,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      tooltipAnchor: [16, -28],
      shadowSize: [41, 41],
    });
    Marker.prototype.options.icon = iconDefault;

    // 2. Inicializar el mapa centrado en coordenadas [lat, lon] y nivel de zoom
    this.map = Leaflet.map('mapId').setView([38.38735, -0.51238], 4);

    // 3. Añadir capa de teselas (Tiles) gratuitas de OpenStreetMap
    Leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'DISM © Ionic Leaflet',
    }).addTo(this.map);

    // 4. Posicionar marcadores con Popups emergentes
    Leaflet.marker([38.38735, -0.51238]).addTo(this.map).bindPopup('Alicante').openPopup();
    Leaflet.marker([41.38113, 2.12244]).addTo(this.map).bindPopup('Barcelona').openPopup();
  }
}
```

---

## 📑 Ejercicio 8: Diseño de API REST con OpenAPI 3.0.0 (`HolaMundo.yaml`)

### 🎯 Objetivo
Aprender el enfoque **API-First (Design-First)** mediante la especificación estándar **OpenAPI 3.0.0** (Swagger). En lugar de escribir el código del servidor primero, se diseña un contrato formal en formato YAML que especifica las rutas, parámetros y respuestas. Este contrato sirve para generar automáticamente documentación interactiva (Swagger UI), clientes y stubs de servidor (Node.js/Express).

---

### 1. Especificación OpenAPI (`HolaMundo.yaml`)
📍 **Archivo:** `DISM8/HolaMundo.yaml` / `HolaMundo.yaml`
```yaml
openapi: 3.0.0
servers:
  - description: Servidor ApiRest DTIC
    url: http://dtic.org/HolaMundo/1.0.0
info:
  description: Esto es un Hola Mundo
  version: "1.0.0"
  title: Hola Mundo Dtic
  contact:
    email: info@dtic.org
  license:
    name: Apache 2.0
    url: 'http://www.apache.org/licenses/LICENSE-2.0.html'

paths:
  /holamundo:
    get:
      tags:
        - HolaMundoServicio
      description: GET Hola Mundo
      parameters:
        - in: query
          name: nombreEntradaHolaMundo
          description: nombre Entrada Hola Mundo
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Respuesta Hola Mundo Correcto
          content:
            application/json:
              schema:
                type: object
                properties:
                  nombre:
                    type: string
                  contador:
                    type: integer
        '400':
          description: Hola Mundo Error
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
```

---

### 2. Desglose del Contrato OpenAPI (Claves para la Defensa)

| Sección | Descripción Técnica |
| :--- | :--- |
| `openapi: 3.0.0` | Especifica la versión del estándar OpenAPI utilizado. |
| `servers` | Define la URL base del servidor donde se desplegará la API (`http://dtic.org/HolaMundo/1.0.0`). |
| `info` | Metadatos descriptivos de la API (título, descripción, versión, contacto y licencia Apache 2.0). |
| `paths` | Catálogo de rutas/endpoints disponibles en el servicio. |
| `/holamundo` (GET) | Operación de consulta categorizada con el tag `HolaMundoServicio`. |
| `parameters` | Parámetro obligatorio por query string (`nombreEntradaHolaMundo` de tipo `string`). |
| `responses` (`200` y `400`) | Esquema de salida estructurado en JSON: código 200 devuelve `{ nombre: string, contador: integer }` y código 400 devuelve `{ message: string }`. |

---

### 3. Herramientas de Visualización y Pruebas en VS Code
1. **OpenAPI Editor (Extensión VS Code):** Permite escribir y validar en tiempo real la sintaxis, sangría e integridad del archivo YAML de OpenAPI.
2. **Swagger UI (Extensión VS Code):** Genera una interfaz web interactiva que interpreta el YAML y permite ejecutar pruebas (*Try it out*) enviando parámetros de consulta y verificando la estructura de las respuestas HTTP.

---

## ⚡ Ejercicio 9: Generación de Stub Node.js/Express mediante Swagger (`Ejercicio9`)

### 🎯 Objetivo
Generar automáticamente la infraestructura completa de un servidor backend en **Node.js con Express** a partir del contrato `HolaMundo.yaml` diseñado en el Ejercicio 8 usando la herramienta CLI `@openapitools/openapi-generator-cli`. Modificar la lógica de negocio en la capa de servicios para que devuelva el mensaje requerido (`"Hola Mundo DISM 2025-2026"` y `contador: 999`) y comprobar su ejecución a través de **Swagger UI** en `http://localhost:8080/api-docs`.

---

### 1. Generación del Proyecto con OpenAPI Generator CLI
```bash
# Instalación global del generador OpenAPI
npm i -g @openapitools/openapi-generator-cli

# Generación del servidor express stub
openapi-generator-cli generate -i ./HolaMundo.yaml -g nodejs-express-server -o ./Ejercicio9

# Instalación de dependencias y arranque
cd Ejercicio9
npm install
npm start
```

---

### 2. Estructura de la Arquitectura Generada

| Directorio / Archivo | Función Arquitectónica |
| :--- | :--- |
| `api/openapi.yaml` | Copia de la especificación OpenAPI utilizada por el validador y Swagger UI. |
| `controllers/` | Controladores Express que reciben la petición HTTP y delegan la ejecución al servicio correspondiente. |
| `services/` | Capa donde reside la **lógica de negocio**. |
| `expressServer.js` | Configuración del servidor Express, middlewares de CORS, parser de JSON, validador `express-openapi-validator` y Swagger UI en `/api-docs`. |
| `index.js` | Punto de entrada que levanta el servidor HTTP en el puerto configurado (8080). |
| `config.js` | Parámetros de configuración de puertos, rutas y directorios. |

---

### 3. Modificación de la Lógica de Negocio (Servicio)
📍 **Archivo:** `Ejercicio9/services/HolaMundoServicioService.js`
```javascript
/* eslint-disable no-unused-vars */
const Service = require('./Service');

/**
* GET Hola Mundo
*
* nombreEntradaHolaMundo String nombre Entrada Hola Mundo
* returns _holamundo_get_200_response
* */
const holamundoGET = ({ nombreEntradaHolaMundo }) => new Promise(
  async (resolve, reject) => {
    try {
      // Retornamos el objeto JSON con contador y nombre según la especificación
      resolve(Service.successResponse({
        contador: 999,
        nombre: 'Hola Mundo DISM 2025-2026',
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);

module.exports = {
  holamundoGET,
};
```

---

### 4. Verificación y Pruebas

#### Prueba interactiva con Swagger UI
- **URL:** `http://localhost:8080/api-docs`
- **Operación:** Desplegar `GET /holamundo`, pulsar en **Try it out**, introducir el parámetro `nombreEntradaHolaMundo: DISM` y pulsar **Execute**.

#### Respuesta obtenida (HTTP 200 OK)
```json
{
  "contador": 999,
  "nombre": "Hola Mundo DISM 2025-2026"
}
```



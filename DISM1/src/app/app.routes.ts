import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('./tabs/tabs.routes').then((m) => m.routes),
  },
  {
    path: 'formulario',
    loadComponent: () => import('./formulario/formulario.page').then( m => m.FormularioPage)
  },
];

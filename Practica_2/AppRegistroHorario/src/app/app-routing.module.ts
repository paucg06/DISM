import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadChildren: () => import('./login/login.module').then(m => m.LoginPageModule)
  },
  {
    path: 'tabs',
    loadChildren: () => import('./tabs/tabs.module').then(m => m.TabsPageModule)
  },
  // Redirecciones directas hacia las pestañas unificadas
  {
    path: 'home',
    redirectTo: 'tabs/home',
    pathMatch: 'full'
  },
  {
    path: 'usuarios',
    redirectTo: 'tabs/usuarios',
    pathMatch: 'full'
  },
  {
    path: 'trabajos',
    redirectTo: 'tabs/trabajos',
    pathMatch: 'full'
  },
  {
    path: 'fichajes',
    redirectTo: 'tabs/fichajes',
    pathMatch: 'full'
  },
  {
    path: 'registrar-fichaje',
    redirectTo: 'tabs/registrar-fichaje',
    pathMatch: 'full'
  },
  {
    path: 'consulta-fichajes',
    redirectTo: 'tabs/consulta-fichajes',
    pathMatch: 'full'
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }

import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'home',
    loadChildren: () => import('./home/home.module').then( m => m.HomePageModule)
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadChildren: () => import('./login/login.module').then( m => m.LoginPageModule)
  },
  {
    path: 'registrar-fichaje',
    loadChildren: () => import('./registrar-fichaje/registrar-fichaje.module').then( m => m.RegistrarFichajePageModule)
  },
  {
    path: 'consulta-fichajes',
    loadChildren: () => import('./consulta-fichajes/consulta-fichajes.module').then( m => m.ConsultaFichajesPageModule)
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }

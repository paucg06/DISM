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
    path: 'home',
    loadChildren: () => import('./home/home.module').then(m => m.HomePageModule)
  },
  {
    path: 'usuarios',
    loadChildren: () => import('./usuarios/usuarios.module').then(m => m.UsuariosPageModule)
  },
  {
    path: 'trabajos',
    loadChildren: () => import('./trabajos/trabajos.module').then(m => m.TrabajosPageModule)
  },
  {
    path: 'fichajes',
    loadChildren: () => import('./fichajes/fichajes.module').then(m => m.FichajesPageModule)
  },
  {
    path: 'registrar-fichaje',
    loadChildren: () => import('./registrar-fichaje/registrar-fichaje.module').then(m => m.RegistrarFichajePageModule)
  },
  {
    path: 'consulta-fichajes',
    loadChildren: () => import('./consulta-fichajes/consulta-fichajes.module').then(m => m.ConsultaFichajesPageModule)
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
export class AppRoutingModule {}

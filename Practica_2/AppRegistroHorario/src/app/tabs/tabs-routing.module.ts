import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      {
        path: 'home',
        loadChildren: () => import('../home/home.module').then(m => m.HomePageModule)
      },
      // Pestañas de Administrador (Azul)
      {
        path: 'usuarios',
        loadChildren: () => import('../usuarios/usuarios.module').then(m => m.UsuariosPageModule)
      },
      {
        path: 'trabajos',
        loadChildren: () => import('../trabajos/trabajos.module').then(m => m.TrabajosPageModule)
      },
      {
        path: 'fichajes',
        loadChildren: () => import('../fichajes/fichajes.module').then(m => m.FichajesPageModule)
      },
      // Pestañas de Empleado (Verde)
      {
        path: 'registrar-fichaje',
        loadChildren: () => import('../registrar-fichaje/registrar-fichaje.module').then(m => m.RegistrarFichajePageModule)
      },
      {
        path: 'consulta-fichajes',
        loadChildren: () => import('../consulta-fichajes/consulta-fichajes.module').then(m => m.ConsultaFichajesPageModule)
      },
      {
        path: '',
        redirectTo: 'home',
        pathMatch: 'full'
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TabsPageRoutingModule {}

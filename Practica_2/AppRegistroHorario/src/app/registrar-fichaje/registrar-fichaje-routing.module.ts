import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { RegistrarFichajePage } from './registrar-fichaje.page';

const routes: Routes = [
  {
    path: '',
    component: RegistrarFichajePage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class RegistrarFichajePageRoutingModule {}

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ConsultaFichajesPage } from './consulta-fichajes.page';

const routes: Routes = [
  {
    path: '',
    component: ConsultaFichajesPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ConsultaFichajesPageRoutingModule {}

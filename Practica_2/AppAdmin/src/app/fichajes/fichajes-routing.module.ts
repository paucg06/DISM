import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { FichajesPage } from './fichajes.page';

const routes: Routes = [
  {
    path: '',
    component: FichajesPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class FichajesPageRoutingModule {}

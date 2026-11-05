import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular/lazy';

import { ConsultaFichajesPageRoutingModule } from './consulta-fichajes-routing.module';

import { ConsultaFichajesPage } from './consulta-fichajes.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ConsultaFichajesPageRoutingModule
  ],
  declarations: [ConsultaFichajesPage]
})
export class ConsultaFichajesPageModule {}

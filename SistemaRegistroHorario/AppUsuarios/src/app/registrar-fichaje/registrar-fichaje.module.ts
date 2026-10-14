import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular/lazy';

import { RegistrarFichajePageRoutingModule } from './registrar-fichaje-routing.module';

import { RegistrarFichajePage } from './registrar-fichaje.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RegistrarFichajePageRoutingModule
  ],
  declarations: [RegistrarFichajePage]
})
export class RegistrarFichajePageModule {}

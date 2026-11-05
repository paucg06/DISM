import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular/lazy';

import { FichajesPageRoutingModule } from './fichajes-routing.module';

import { FichajesPage } from './fichajes.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    FichajesPageRoutingModule
  ],
  declarations: [FichajesPage]
})
export class FichajesPageModule {}

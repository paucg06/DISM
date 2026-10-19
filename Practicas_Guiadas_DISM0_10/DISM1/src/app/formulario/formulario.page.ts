import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar, IonToggle, IonList, IonItem, IonButton } from '@ionic/angular';

@Component({
  selector: 'app-formulario',
  templateUrl: './formulario.page.html',
  styleUrls: ['./formulario.page.scss'],
  imports: [IonContent, IonHeader, IonTitle, IonToolbar, IonToggle, IonList, IonItem, CommonModule, FormsModule, IonButton]
})
export class FormularioPage implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}

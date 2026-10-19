import { Component } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonList, IonItem, IonLabel } from '@ionic/angular';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss'],
  imports: [IonItem, IonList, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonLabel]
})
export class Tab2Page {
  lista = [
    { name: 'Sandía' },
    { name: 'Naranja' },
    { name: 'Fresa' },
    { name: 'Melón' },
    { name: 'Manzana' }
  ];
  constructor() {}
}

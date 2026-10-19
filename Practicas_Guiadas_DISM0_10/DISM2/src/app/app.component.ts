import { Component } from '@angular/core';
import { IonIcon, IonApp, IonRouterOutlet, IonItem, IonSplitPane, IonMenu,
  IonHeader, IonToolbar, IonTitle, IonLabel, IonContent, IonList, IonMenuToggle } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { helpCircle, home } from 'ionicons/icons';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  imports: [RouterModule, IonItem, IonApp, IonRouterOutlet, IonSplitPane, IonMenu, IonHeader, IonToolbar, IonTitle,
    IonLabel, IonContent, IonList, IonMenuToggle, IonIcon],
})
export class AppComponent {
  constructor() {
    addIcons({ helpCircle, home });
  }
}


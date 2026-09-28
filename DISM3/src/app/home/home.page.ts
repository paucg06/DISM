import { Component } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonList,
  IonItem, IonAvatar, IonImg, IonLabel, IonButton } from '@ionic/angular';
import { HttpService } from '../services/http';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonButton, IonLabel, IonImg, IonAvatar, IonItem, IonList, IonHeader, IonToolbar, IonTitle, IonContent],
})
export class HomePage {
  usuarios: any[] = [];

  constructor(private http: HttpService) {}

  async cargarUsuarios() {
    try {
      const res: any = await firstValueFrom(this.http.loadUsers());
      this.usuarios = res.results;
    } catch (error) {
      console.error(error);
    }
  }
}

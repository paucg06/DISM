import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TrabajosPage } from './trabajos.page';

describe('TrabajosPage', () => {
  let component: TrabajosPage;
  let fixture: ComponentFixture<TrabajosPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(TrabajosPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

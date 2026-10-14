import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FichajesPage } from './fichajes.page';

describe('FichajesPage', () => {
  let component: FichajesPage;
  let fixture: ComponentFixture<FichajesPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(FichajesPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

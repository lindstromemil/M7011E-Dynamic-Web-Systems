import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BreweryComponent } from './brewery.component';

describe('BreweryComponent', () => {
  let component: BreweryComponent;
  let fixture: ComponentFixture<BreweryComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BreweryComponent]
    });
    fixture = TestBed.createComponent(BreweryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

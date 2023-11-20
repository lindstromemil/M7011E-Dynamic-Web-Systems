import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IndividualEntriesComponent } from './individual-entries.component';

describe('IndividualEntriesComponent', () => {
  let component: IndividualEntriesComponent;
  let fixture: ComponentFixture<IndividualEntriesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [IndividualEntriesComponent]
    });
    fixture = TestBed.createComponent(IndividualEntriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

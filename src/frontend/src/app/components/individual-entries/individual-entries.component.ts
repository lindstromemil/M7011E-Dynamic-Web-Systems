import { Component, OnInit, inject } from '@angular/core';
import { BeverageService } from 'src/app/services/beverage.service';
import { Beverage } from 'src/app/models/beverage.model';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTabsModule } from '@angular/material/tabs';
@Component({
  selector: 'app-individual-entries',
  templateUrl: './individual-entries.component.html',
  styleUrls: ['./individual-entries.component.css']
})

export class IndividualEntriesComponent implements OnInit {

  beverage: Beverage = {
    _id: { $oid: '' },
    name: '',
    description: '',
    image_path: '',
    bitterness: 0,
    fullness: 0,
    sweetness: 0,
    abv: 0,
    beverageType: '',
    country: '',
    brand: {
      _id: { $oid: '' },
      name: '',
      description: ''
    }
  };

  constructor(
    private beverageService: BeverageService,
    private titleService: Title
  ) { }

  private route = inject(ActivatedRoute)

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id == 'test') {
      this.beverageService.getBeverages().subscribe((data: Beverage[]) => {
        this.beverage = data[0];
        this.titleService.setTitle(this.beverage.name);
      });
    }
  }

}

import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '../services/user.service';
import { BeverageService } from '../services/beverage.service';
import { Activity, Rating } from '../models/rating.model';
import { Beverage } from '../models/beverage.model';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'],
})
export class ProfileComponent implements OnInit {
  activity: Activity[] = [];

  constructor(
    private router: Router,
    private beverageAPI: BeverageService,
    private userAPI: UserService
  ) {}
  name: string = inject(ActivatedRoute).snapshot.paramMap.get('username') || '';

  ngOnInit() {
    this.load_content();
  }

  load_content() {
    this.userAPI.get_all_user_ratings(this.name).subscribe(
      (rating: Rating[]) => {
        for (let i = 0; i < rating.length; i++) {
          this.beverageAPI
            .get_beverage(rating[i].beverage_id.$oid.toString())
            .subscribe(
              (beverage: Beverage) => {
                let activity: Activity = {
                  beverage: beverage,
                  score: rating[i].score,
                  created_at: rating[i].created_at.$date
                    .toString()
                    .slice(0, 10),
                };
                this.activity.push(activity);
              },
              (err) => {
                console.error(err.error);
              }
            );
        }
      },
      (err) => {
        console.error(err.error);
      }
    );
  }

  navigateToBeveragePage(name: string) {
    console.log(name);
    this.router.navigate(['beverage/' + name]);
  }
}

import {Component, inject, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {BeverageService} from "../services/beverage.service";
import {UserService} from "../services/user.service";
import {Beverage} from "../models/beverage.model";
import {Activity, Rating} from "../models/rating.model";
import {PlanningService} from "../services/planning.service";
import {User} from "../models/user.model";
import {Planning} from "../models/planning.model";

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrl: './list.component.css'
})
export class ListComponent implements OnInit {
  beers_had: Beverage[] = [];
  beers_planned: Beverage[] = [];

  constructor(
    private router: Router,
    private beverageAPI: BeverageService,
    private userAPI: UserService,
    private planningAPI: PlanningService
  ) {
  }

  private name: string = inject(ActivatedRoute).snapshot.paramMap.get('username') || "";

  ngOnInit() {
    this.load_content();
  }

  load_content() {
    this.userAPI.get_user(this.name).subscribe(
      (user: User) => {
        this.planningAPI.get_all_plannings(user._id.$oid.toString()).subscribe(
          (planning: Planning[]) => {
            for (let i = 0; i < planning.length; i++) {
              this.beverageAPI.get_beverage(planning[i].beverage_id).subscribe(
                (beverage: Beverage) => {
                  this.beers_planned.push(beverage);
                },
                err => {
                  console.error(err.error)
                }
              )
            }
          },
          err => {
            console.error(err.error)
          }
        )
      },
      err => {
        console.error(err.error)
      }
    )
    this.userAPI.get_all_user_ratings(this.name).subscribe(
      (rating: Rating[]) => {
        for(let i = 0; i < rating.length; i++) {
          this.beverageAPI.get_beverage(rating[i].beverage_id.$oid.toString()).subscribe(
          (beverage: Beverage) => {
            this.beers_had.push(beverage);
          },
          err => {
            console.error(err.error)
          }
        )
        }
      },
      err => {
        console.error(err.error)
      }
    )
  }

  round(value: number, precision: number) {
    var multiplier = Math.pow(10, precision.valueOf() || 0);
    return Math.round(value.valueOf() * multiplier) / multiplier;
  }
  convertToPercentage(str: number): number {
    const percentage = str * 100;
    return this.round(percentage, 1);
  }

  navigateToBeveragePage(name: string) {
    console.log(name);
    this.router.navigate(['entry']);
  }

}

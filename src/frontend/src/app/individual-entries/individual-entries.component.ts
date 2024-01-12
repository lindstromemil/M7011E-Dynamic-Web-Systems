import { Component, NgModule, OnInit, inject } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { BeverageService } from '../services/beverage.service';
import { Beverage } from '../models/beverage.model';
import { BrandService } from '../services/brand.service';
import { Brand } from '../models/brand.model';
import { Title } from '@angular/platform-browser';
import { RatingsService } from '../services/ratings.service';
import { Rating } from '../models/rating.model';
import { Router, RouterModule } from '@angular/router';
import { PlanningService } from '../services/planning.service';
import { Planning } from '../models/planning.model';
import { UserService } from '../services/user.service';
import { User } from '../models/user.model';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-individual-entries',
  templateUrl: './individual-entries.component.html',
  styleUrls: ['./individual-entries.component.css'],
})
export class IndividualEntriesComponent implements OnInit {
  beverage: Beverage | null = null;
  brand: Brand | null = null;
  ratings: Rating[] = [];
  averageRating: number = -1;
  isLoading = true;
  brandRecommendations: Beverage[] = [];
  typeRecommendations: Beverage[] = [];
  recommendedSize: number = 6;

  createDialogOpen: boolean = false;
  updateDialogOpen: boolean = false;

  userStatus: string = 'Not logged in';
  usersRating: Rating = {
    _id: null,
    beverage_id: '',
    user_id: '',
    score: 1,
    comment: '',
    created_at: null,
  };

  private beverageId: string = '';
  constructor(
    private beverageAPI: BeverageService,
    private brandAPI: BrandService,
    private ratingAPI: RatingsService,
    private userAPI: UserService,
    private planningAPI: PlanningService,
    private titleService: Title,
    private router: Router,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.userStatus = 'Not logged in';
    this.route.params.subscribe((params) => {
      this.beverageId = params['id'];
      this.loadContent();
    });
  }

  private loadContent() {
    this.isLoading = true;
    window.scrollTo(0, 0);
    this.beverageAPI
      .get_beverage(this.beverageId)
      .subscribe((beverageData: Beverage) => {
        this.beverage = beverageData;
        console.log(beverageData);
        this.titleService.setTitle(this.beverage.name);
        this.brandAPI
          .get_brand(this.beverage.brand_id.$oid)
          .subscribe((brandData: Brand) => {
            this.brand = brandData;
            console.log(brandData);
          });
        this.ratingAPI
          .get_all_beverage_ratings(this.beverage._id.$oid)
          .subscribe((ratings) => {
            this.ratings = ratings;
            console.log(ratings);
            let sum = 0;
            this.userAPI.get_me().subscribe((user: User) => {
              console.log('user');
              console.log(user);
              if (user != null) {
                this.userStatus = 'Logged in';
              }
              if (ratings.length > 0) {
                for (let i = 0; i < ratings.length; i++) {
                  if (
                    this.userStatus == 'Logged in' &&
                    ratings[i].user_id.$oid == user._id.$oid
                  ) {
                    this.userStatus = 'Rated';
                    this.usersRating = ratings[i];
                  }
                  sum += ratings[i].score;
                }
                this.averageRating = sum / ratings.length;
              } else {
                this.averageRating = -1;
              }
              if (this.userStatus == 'Logged in') {
                this.planningAPI
                  .get_all_plannings(user._id.$oid)
                  .subscribe((plannings) => {
                    for (let i = 0; i < plannings.length; i++) {
                      if (plannings[i].beverage_id == this.beverage?._id.$oid) {
                        this.userStatus = 'Planned';
                        break;
                      }
                    }
                  });
              }
            });
            this.isLoading = false;
          });
        this.beverageAPI
          .get_all_beverages(
            1,
            this.recommendedSize,
            this.beverage.beverageType
          )
          .subscribe((beverages) => {
            this.typeRecommendations = beverages;
            console.log(beverages);
          });
        this.beverageAPI
          .get_all_beverages(
            1,
            this.recommendedSize,
            this.beverage.brand_id.$oid
          )
          .subscribe((beverages) => {
            this.brandRecommendations = beverages;
            console.log(beverages);
          });
      });
  }

  addToPlanning() {
    this.userAPI.get_me().subscribe((user: User) => {
      this.planningAPI
        .create_planning(user._id.$oid, this.beverage?._id.$oid)
        .subscribe((result: string) => {
          console.log(result);
          this.userStatus = 'Planned';
        });
    });
  }

  openCreateDialog() {
    this.createDialogOpen = true;
  }

  submitCreateDialog() {
    console.log(this.usersRating?.comment);
    console.log(this.usersRating?.score);
    this.usersRating.beverage_id = this.beverage?._id.$oid;
    this.ratingAPI
      .create_rating(
        this.beverage?.name || '',
        this.usersRating.score,
        this.usersRating.comment
      )
      .subscribe((result: string) => {
        console.log(result);
        this.loadContent();
      });
    this.createDialogOpen = false;
    this.userStatus = 'Rated';
  }

  closeCreateDialog() {
    this.createDialogOpen = false;
  }

  openUpdateDialog() {
    this.updateDialogOpen = true;
  }

  submitUpdateDialog() {
    console.log(this.usersRating?.comment);
    console.log(this.usersRating?.score);
    this.usersRating.beverage_id = this.beverage?._id.$oid;
    this.ratingAPI
      .update_rating(
        this.usersRating._id.$oid,
        this.usersRating.score,
        this.usersRating.comment
      )
      .subscribe((result: string) => {
        console.log(result);
        this.loadContent();
      });
    this.updateDialogOpen = false;
    this.userStatus = 'Rated';
  }

  closeUpdateDialog() {
    this.updateDialogOpen = false;
  }

  isScoreValid(): boolean {
    var score = this.usersRating.score;
    return score != null && score >= 1 && score <= 10;
  }

  round(value: number, precision: number) {
    var multiplier = Math.pow(10, precision.valueOf() || 0);
    return Math.round(value.valueOf() * multiplier) / multiplier;
  }

  convertToPercentage(str: number): number {
    const percentage = str * 100;
    return this.round(percentage, 1);
  }
}

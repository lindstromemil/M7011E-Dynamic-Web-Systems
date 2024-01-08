import {Component, inject, OnInit} from '@angular/core';
import {Rating, Review} from "../models/rating.model";
import {ActivatedRoute, Router} from "@angular/router";
import {BeverageService} from "../services/beverage.service";
import {UserService} from "../services/user.service";
import {Beverage} from "../models/beverage.model";
import {RatingsService} from "../services/ratings.service";
import {Like} from "../models/like.model";
import {LikeService} from "../services/like.service";

@Component({
  selector: 'app-reviews',
  templateUrl: './reviews.component.html',
  styleUrl: './reviews.component.css'
})
export class ReviewsComponent implements OnInit {

  reviews: Review[] = [];

  constructor(
    private router: Router,
    private beverageAPI: BeverageService,
    private userAPI: UserService,
    private ratingAPI: RatingsService,
    private likeAPI: LikeService
  ) {
  }

  private name: string = inject(ActivatedRoute).snapshot.paramMap.get('username') || "";

  ngOnInit() {
    this.load_content();
  }

  load_content() {
    this.userAPI.get_all_user_ratings(this.name).subscribe(
      (rating: Rating[]) => {
        for (let i = 0; i < rating.length; i++) {
          if (rating[i].comment !== "") {
            this.beverageAPI.get_beverage(rating[i].beverage_id.$oid.toString()).subscribe(
              (beverage: Beverage) => {
                this.ratingAPI.get_all_rating_likes(rating[i]._id.$oid.toString()).subscribe(
                  (likes: Like[]) => {
                    let review: Review = {
                      ratingId: rating[i]._id.$oid.toString(),
                      beverage: beverage,
                      score: rating[i].score,
                      comment: rating[i].comment,
                      likes: likes.length,
                      created_at: rating[i].created_at.$date.toString().slice(0, 10)
                    }
                    this.reviews.push(review);
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
          }
        }
      },
      err => {
        console.error(err.error)
      }
    )
  }

  likeReview(rating_id: string) {
    this.likeAPI.create_like(rating_id).subscribe(
      () => {
        for(let i = 0; i < this.reviews.length; i++) {
          if (this.reviews[i].ratingId === rating_id) {
            this.reviews[i].likes += 1;
          }
        }
      },
      err => {
        console.error(err.error)
      }
    )
  }

  navigateToBeveragePage(name: string) {
    console.log(name);
    this.router.navigate(['beverage/'+name]);
  }

}

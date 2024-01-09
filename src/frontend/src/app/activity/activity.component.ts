import {Component, OnInit} from '@angular/core';
import {UserService} from 'src/app/services/user.service'
import {User} from '../models/user.model';
import {AuthService} from "../services/auth.service";
import {Router} from "@angular/router";
import {BeverageService} from "../services/beverage.service";
import {RatingsService} from "../services/ratings.service";
import {LikeService} from "../services/like.service";
import {Rating, Review} from "../models/rating.model";
import {Beverage} from "../models/beverage.model";
import {Like} from "../models/like.model";
import {FollowService} from "../services/follow.service";

@Component({
  selector: 'app-activity',
  templateUrl: './activity.component.html',
  styleUrls: ['./activity.component.css'],
})
export class ActivityComponent implements OnInit {
  reviews: Review[] = [];


  constructor(
    private router: Router,
    private beverageAPI: BeverageService,
    private userAPI: UserService,
    private ratingAPI: RatingsService,
    private likeAPI: LikeService,
    private followAPI: FollowService,
    private authService: AuthService
  ) {
    authService.ngOnInit();
  }

  ngOnInit(): void {
    this.userAPI.get_me().subscribe(
      (user: User) => {
        this.followAPI.get_all_follows(user._id.$oid.toString()).subscribe(
          (follows: User[]) => {
            for (let y = 0; y < follows.length; y++) {
              this.userAPI.get_all_user_ratings(follows[y].username).subscribe(
                (rating: Rating[]) => {
                  for (let i = 0; i < rating.length; i++) {
                    if (rating[i].comment !== "") {
                      this.beverageAPI.get_beverage(rating[i].beverage_id.$oid.toString()).subscribe(
                        (beverage: Beverage) => {
                          this.ratingAPI.get_all_rating_likes(rating[i]._id.$oid.toString()).subscribe(
                            (likes: Like[]) => {
                              let review: Review = {
                                username: follows[y].username,
                                ratingId: rating[i]._id.$oid.toString(),
                                beverage: beverage,
                                score: rating[i].score,
                                comment: rating[i].comment,
                                likes: likes.length,
                                created_at: rating[i].created_at.$date.toString().slice(0, 10)
                              }
                              this.reviews = this.insertIntoSortedArray(this.reviews, review)
                              //this.reviews.push(review);
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
          },
          err => {
            console.error(err.error)
          }
        )
      },
      err => {
        console.error("Could not find me:" + err);
      }
    )
  }

  insertIntoSortedArray(arr: Review[], value: Review): Review[] {
    let i = arr.length - 1;

    while (i >= 0 && arr[i].created_at < value.created_at) {
      arr[i + 1] = arr[i];
      i--;
    }

    arr[i + 1] = value;

    return arr;
  }

  navigateToBeveragePage(name: string) {
    console.log(name);
    this.router.navigate(['beverage/'+name]);
  }

  navigateToProfilePage(name: string) {
    this.router.navigate(['user/'+name]);
  }

  likeReview(rating_id: string) {
    this.likeAPI.create_like(rating_id).subscribe(
      () => {
        for (let i = 0; i < this.reviews.length; i++) {
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
}

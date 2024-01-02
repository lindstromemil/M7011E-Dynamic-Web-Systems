import {Component, HostListener, inject, OnInit} from '@angular/core';
import {FormControl} from "@angular/forms";
import {ActivatedRoute, Router} from "@angular/router";
import {debounceTime} from "rxjs";
import {FollowService} from "../services/follow.service";
import {Follower, Follows} from "../models/follow.model";
import {UserService} from "../services/user.service";
import {User} from "../models/user.model";

@Component({
  selector: 'app-social',
  templateUrl: './social.component.html',
  styleUrl: './social.component.css'
})
export class SocialComponent implements OnInit {
  follows: User[] = [];
  followers: User[] = [];

  constructor(
    private router: Router,
    private followAPI: FollowService,
    private userAPI: UserService
  ) {
  }

  private name: string = inject(ActivatedRoute).snapshot.paramMap.get('username') || "";

  ngOnInit() {
    this.load_content();
  }


  load_content() {
    this.userAPI.get_user(this.name).subscribe(
      (user: User) => {
        this.followAPI.get_all_followers(user._id.$oid.toString()).subscribe(
          (followers: User[]) => {
            this.followers = followers;
          },
          err => {
            console.error(err.error)
          }
        )

        this.followAPI.get_all_follows(user._id.$oid.toString()).subscribe(
          (follows: User[]) => {
            this.follows = follows;
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

  navigateToProfilePage(name: string) {
    console.log(name);
    this.router.navigate(['user/'+name]);
  }
}

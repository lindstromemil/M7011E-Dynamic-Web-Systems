import {
  booleanAttribute,
  Component,
  inject,
  Input,
  OnInit,
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '../services/user.service';
import { User } from '../models/user.model';
import { Beverage } from '../models/beverage.model';
import { FollowService } from '../services/follow.service';

@Component({
  selector: 'app-profile-bar',
  templateUrl: './profile-bar.component.html',
  styleUrl: './profile-bar.component.css',
})
export class ProfileBarComponent implements OnInit {
  constructor(
    private router: Router,
    private userAPI: UserService,
    private followAPI: FollowService
  ) {}

  name: string = inject(ActivatedRoute).snapshot.paramMap.get('username') || '';
  description: string = '';
  imageSrc: string = 'assets/images/logo.png';
  isMyProfile: boolean = true;
  isFollowing: boolean = false;
  finished_loading: boolean = false;

  @Input({ transform: booleanAttribute }) overviewSelected!: boolean;
  @Input({ transform: booleanAttribute }) listSelected!: boolean;
  @Input({ transform: booleanAttribute }) socialSelected!: boolean;
  @Input({ transform: booleanAttribute }) reviewsSelected!: boolean;

  ngOnInit() {
    this.userAPI.get_me().subscribe(
      (user: User) => {
        this.isMyProfile = user.username === this.name;
        this.followAPI.get_all_follows(user._id.$oid.toString()).subscribe(
          (follows: User[]) => {
            for (let i = 0; i < follows.length; i++) {
              if (follows[i].username === this.name) {
                this.isFollowing = true;
              }
            }
            this.finished_loading = true;
          },
          (err) => {
            console.error(err.error);
          }
        );
      },
      (err) => {
        console.error(err.error);
      }
    );
    this.userAPI.get_user(this.name).subscribe((user: User) => {
      this.imageSrc = user.profile.image_path;
      this.description = user.profile.description;
    });
  }

  overview(): void {
    this.router.navigate(['user/' + this.name]);
  }

  list(): void {
    this.router.navigate(['user/' + this.name + '/list']);
  }

  social(): void {
    this.router.navigate(['user/' + this.name + '/social']);
  }

  reviews(): void {
    this.router.navigate(['user/' + this.name + '/reviews']);
  }

  follow(): void {
    this.followAPI.create_follow(this.name).subscribe(
      () => {
        this.isFollowing = true;
      },
      (err) => {
        console.error(err.error);
      }
    );
  }

  unfollow(): void {
    this.followAPI.delete_follow(this.name).subscribe(
      () => {
        this.isFollowing = false;
      },
      (err) => {
        console.error(err.error);
      }
    );
  }
}

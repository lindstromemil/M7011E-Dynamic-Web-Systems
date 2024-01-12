import { Component, Input, booleanAttribute, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { User } from '../models/user.model';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
})
export class NavbarComponent implements OnInit {
  imageSrc = 'assets/defaultAvatar.png';
  loggedIn = false;

  constructor(
    private router: Router,
    private cookieService: CookieService,
    private userAPI: UserService
  ) {}

  @Input({ transform: booleanAttribute }) firstSelected!: boolean;
  @Input({ transform: booleanAttribute }) secondSelected!: boolean;
  @Input({ transform: booleanAttribute }) thirdSelected!: boolean;

  ngOnInit(): void {
    if (this.cookieService.check('token')) {
      this.loggedIn = true;
      this.userAPI.get_me().subscribe((user: User) => {
        if (user.profile.image_path !== '') {
          this.imageSrc = user.profile.image_path;
        }
      });
    } else {
      this.loggedIn = false;
      this.imageSrc = 'assets/defaultAvatar.png';
    }
    console.log(this.imageSrc);
    console.log(this.loggedIn);
  }

  logout(): void {
    this.cookieService.deleteAll();
    this.imageSrc = 'assets/defaultAvatar.png';
    this.router.navigate(['browse']);
  }

  settings(): void {
    this.router.navigate(['settings']);
  }

  navigateToActivity(): void {
    this.router.navigate(['activity']);
  }

  navigateToProfilePage(): void {
    this.userAPI.get_me().subscribe(
      (user: User) => {
        this.router.navigate(['user/' + user.username]);
      },
      (err) => {
        console.error('Could not find me:' + err);
      }
    );
  }

  navigateToBeverageList(): void {
    this.userAPI.get_me().subscribe(
      (user: User) => {
        this.router.navigate(['user/' + user.username + '/list']);
      },
      (err) => {
        console.error('Could not find me:' + err);
      }
    );
  }

  navigateToBrowse(): void {
    this.router.navigate(['browse']);
  }

  navigateToLogin(): void {
    this.router.navigate(['login']);
  }
}

import { Component, Input, booleanAttribute } from '@angular/core';
import { Router } from '@angular/router';
import {CookieService} from 'ngx-cookie-service';
import {User} from "../models/user.model";
import {UserService} from "../services/user.service";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  constructor(
    private router: Router,
    private cookieService: CookieService,
    private userAPI: UserService
    ) {
  }

  @Input({ transform: booleanAttribute }) firstSelected!: boolean;
  @Input({ transform: booleanAttribute }) secondSelected!: boolean;
  @Input({ transform: booleanAttribute }) thirdSelected!: boolean;

  logout(): void {
    this.cookieService.set('token', "");
    this.cookieService.set('token', "");
    this.cookieService.set('token', "");
    this.cookieService.set('token', "");

    this.router.navigate(['login']);
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
        this.router.navigate(['user/'+user.username]);
      },
      err => {
        console.error("Could not find me:" + err);
      }
    )
  }

  navigateToBrowse(): void {
      this.router.navigate(['browse']);
  }
}

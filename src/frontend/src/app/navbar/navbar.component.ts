import { Component, Input, booleanAttribute } from '@angular/core';
import { Router } from '@angular/router';
import {CookieService} from 'ngx-cookie-service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  constructor(
    private router: Router,
    private cookieService: CookieService
    ) {
  }

  @Input({ transform: booleanAttribute }) firstSelected!: boolean;
  @Input({ transform: booleanAttribute }) secondSelected!: boolean;
  @Input({ transform: booleanAttribute }) thirdSelected!: boolean;

  logout(): void {
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
      this.router.navigate(['profile']);
  }

  navigateToBrowse(): void {
      this.router.navigate(['browse']);
  }
}

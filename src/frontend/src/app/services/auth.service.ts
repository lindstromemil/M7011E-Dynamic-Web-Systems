import {Injectable, OnInit} from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";
import {UserService} from "./user.service";

@Injectable({
  providedIn:'root'
})
export class AuthService implements OnInit {

    constructor(
      private cookieService: CookieService,
      private router: Router,
      private userService: UserService
    ) {

    }

    ngOnInit(): void {
      let username = this.cookieService.get('token');
      if (!username) {
        this.router.navigate(['login']);
      } else {
        this.userService.get_me().subscribe(
          () => {console.log("valid token")},
          err => {
            this.cookieService.set('token', "");
            this.router.navigate(['login']);
          }
        )
      }
    }
  }

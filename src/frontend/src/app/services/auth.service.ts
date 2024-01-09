import {Injectable, OnInit} from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";
import {UserService} from "./user.service";
import {User} from "../models/user.model";

@Injectable({
  providedIn:'root'
})
export class AuthService implements OnInit {
    user_id = "";
    username: string = "";
    constructor(
      private cookieService: CookieService,
      private router: Router,
      private userService: UserService
    ) {

    }

    ngOnInit(): void {
      let username = this.cookieService.get('token');
      if (!username || username === "") {
        this.router.navigate(['login']);
      } else {
        this.userService.get_me().subscribe(
          (user: User) => {
            this.user_id = user._id.$oid.toString();
            this.username = user.username;
          },
          err => {
            this.cookieService.set('token', "");
            this.router.navigate(['login']);
          }
        )
      }
    }


  }

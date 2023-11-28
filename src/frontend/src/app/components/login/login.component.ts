import { Component, Inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from 'src/app/services/user.service'
import { User } from 'src/app/models/user.model';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  login: boolean = true;
  username: string = '';
  password: string = '';

  constructor(
    private router: Router,
    private userAPI: UserService,
    private cookieService: CookieService
  ) {
  }

  ngOnInit(): void {
    let username = this.cookieService.get('_id');
    if (username !== "") {
      this.router.navigate(['activity']);
    }
  }


  loginUser() {
    // Login user
    // Send to home page
    if (this.username === "" || this.password === "") {
      return
    }
    this.userAPI.login_user(this.username, this.password).subscribe(
      (userResponse: User) => {
        const stringId = userResponse._id.$oid.toString();
        this.cookieService.set('_id', stringId);
        this.router.navigate(['activity']);
      },
      err => {
        console.error("Could not login:" + err);
      }
    )
  }

  registerUser() {
    // Register user
    // Send to home page
    if (this.username === "" || this.password === "") {
      return
    }
    this.userAPI.create_user(this.username, this.password).subscribe(
      (userResponse: User) => {
        const stringId = userResponse._id.$oid.toString();
        this.cookieService.set('_id', stringId);
        this.router.navigate(['activity']);
      },
      err => {
        console.error("Could not login:" + err);
      }
    )
  }

  switchRegLog() {
    this.login = !this.login;
  }
}

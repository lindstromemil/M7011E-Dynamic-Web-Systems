import {Component} from '@angular/core';
import {UserService} from "../services/user.service";
import {AuthService} from "../services/auth.service";
import {CookieService} from "ngx-cookie-service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-profile',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent {
  newPassword: string = '';
  passwordChanged: boolean = false;

  constructor(
    private userAPI: UserService,
    private authService: AuthService,
    private cookieService: CookieService,
    private router: Router
  ) {
    authService.ngOnInit();
  }

  deleteProfile() {
    this.userAPI.delete_user(this.authService.username).subscribe(
      () => {
        this.cookieService.set('token', "");
        this.router.navigate(['login']);
      },
      err => {
        console.error(err.error)
      }
    )
  }

  changePassword() {
    if (this.newPassword === "") {
      return
    }
    this.userAPI.update_password(this.newPassword, this.authService.user_id).subscribe(
      () => {
        this.passwordChanged = true;
      },
      err => {
        console.error(err.error)
      }
    )
  }
}

import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'frontend';

  constructor(
    private cookieService: CookieService,
    private router: Router,
  ) {

  }

  ngOnInit(): void {
    let username = this.cookieService.get('_id');
    if (username === "") {
      this.router.navigate(['login']);
    }
  }
}

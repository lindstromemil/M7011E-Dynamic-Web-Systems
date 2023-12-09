import { Component, OnInit } from '@angular/core';
import {UserService} from 'src/app/services/user.service'
import { User } from '../models/user.model';

@Component({
  selector: 'app-activity',
  templateUrl: './activity.component.html',
  styleUrls: ['./activity.component.css'],
})
export class ActivityComponent implements OnInit {
  username: string = "";


  constructor(
    private userAPI: UserService
  ) {

  }

  ngOnInit(): void {
    this.userAPI.get_me().subscribe(
      (user: User) => {
        this.username = user.username;
      },
      err => {
        console.error("Could not find me:" + err);
      }
    )
  }
}

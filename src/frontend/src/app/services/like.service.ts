import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {Beverage} from 'src/app/models/beverage.model';
import { environment } from 'src/environments/environment';
import {Like} from "../models/like.model";
import {User} from "../models/user.model";
import {CookieService} from "ngx-cookie-service";

@Injectable({
  providedIn:'root'
})
export class LikeService {

    constructor(
        private http: HttpClient,
        private cookieService: CookieService
    ) {

    }

    create_like(rating_id: string): Observable<string> {
      const header: {Authorization: string} = { 'Authorization': `Bearer ${this.cookieService.get('token')}` }
      const body = {
        'rating_id': rating_id
      }

      return this.http.post<string>(environment.baseUrl+"/likes", body,{ headers: header });
    }
  }

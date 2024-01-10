import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {Beverage} from 'src/app/models/beverage.model';
import { environment } from 'src/environments/environment';
import {Like} from "../models/like.model";
import {CookieService} from "ngx-cookie-service";

@Injectable({
  providedIn:'root'
})
export class RatingsService {

    constructor(
        private http: HttpClient,
        private cookieService: CookieService
    ) {

    }

    delete_rating(rating_id: string): Observable<string> {
      const header: {Authorization: string} = { 'Authorization': `Bearer ${this.cookieService.get('token')}` }

      return this.http.delete<string>(environment.baseUrl+"/ratings/"+rating_id, { headers: header });
    }

    get_all_rating_likes(rating_id: string): Observable<Like[]> {
      return this.http.get<Like[]>(environment.baseUrl+"/rating/"+rating_id+"/likes");
    }
  }

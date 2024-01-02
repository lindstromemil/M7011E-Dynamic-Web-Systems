import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {Beverage} from 'src/app/models/beverage.model';
import { environment } from 'src/environments/environment';
import {Like} from "../models/like.model";

@Injectable({
  providedIn:'root'
})
export class RatingsService {

    constructor(
        private http: HttpClient,
    ) {

    }

    get_all_rating_likes(rating_id: string): Observable<Like[]> {
      return this.http.get<Like[]>(environment.baseUrl+"/rating/"+rating_id+"/likes");
    }
  }

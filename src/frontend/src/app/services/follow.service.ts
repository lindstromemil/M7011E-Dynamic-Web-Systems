import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import {User} from "../models/user.model";
import {CookieService} from "ngx-cookie-service";

@Injectable({
  providedIn:'root'
})
export class FollowService {

    constructor(
        private http: HttpClient,
        private cookieService: CookieService
    ) {

    }

    create_follow(target_user: string): Observable<string> {
      const header: {Authorization: string} = { 'Authorization': `Bearer ${this.cookieService.get('token')}` }
      const body = {
        'target_username': target_user
      }

      return this.http.post<string>(environment.baseUrl+"/follows", body,{ headers: header });
    }

    delete_follow(target_user: string): Observable<string> {
      const header: {Authorization: string} = { 'Authorization': `Bearer ${this.cookieService.get('token')}` }

      return this.http.delete<string>(environment.baseUrl+"/follows/"+target_user,{ headers: header });
    }

    get_all_followers(personId: string): Observable<User[]> {
      return this.http.get<User[]>(environment.baseUrl+"/followers?&q="+personId);
    }

    get_all_follows(personId: string): Observable<User[]> {
      return this.http.get<User[]>(environment.baseUrl+"/follows?&q="+personId);
    }
  }

import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {Token, User} from 'src/app/models/user.model';
import { environment } from 'src/environments/environment';
import {CookieService} from 'ngx-cookie-service';
import {Rating} from "../models/rating.model";

@Injectable({
  providedIn:'root'
})
export class AdminService {

    constructor(
        private http: HttpClient,
        private cookieService: CookieService
    ) {

    }

    create_user(username: string, password: string): Observable<Token> {
        const body = {
          "image_path": "----",
          "description": "nice kille",
          "username": username,
          "password": password
        };
        return this.http.post<Token>(environment.baseUrl+"/users", body);
    }

    get_user(username: string): Observable<User> {
      return this.http.get<User>(environment.baseUrl+"/users/"+username);
    }

    login_user(username: string, password: string): Observable<Token> {
      return this.http.get<Token>(environment.baseUrl+"/users/login/"+username+":"+password);
    }

    admin_me(): Observable<boolean> {
      const header: {Authorization: string} = { 'Authorization': `Bearer ${this.cookieService.get('token')}` }

      return this.http.get<boolean>(environment.baseUrl+"/admins/me", { headers: header });
    }

    update_password(newPass: string, userId: string): Observable<string> {
      const header: {Authorization: string} = { 'Authorization': `Bearer ${this.cookieService.get('token')}` }
      const body = {
      'password': `${newPass}`
      };
      return this.http.patch<string>(environment.baseUrl+"/users/"+userId, body, { headers: header });
    }

    delete_user(username: string): Observable<string> {
      const header: {Authorization: string} = { 'Authorization': `Bearer ${this.cookieService.get('token')}` }
      return this.http.delete<string>(environment.baseUrl+"/users/"+username, { headers: header });
    }

    get_all_user_ratings(username: string): Observable<Rating[]> {
      return this.http.get<Rating[]>(environment.baseUrl+"/users/"+username+"/ratings");
    }
  }

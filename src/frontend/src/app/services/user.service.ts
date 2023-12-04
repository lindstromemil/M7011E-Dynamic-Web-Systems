import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from 'src/app/models/user.model';
import { environment } from 'src/environments/environment';
import {CookieService} from 'ngx-cookie-service';

@Injectable({
  providedIn:'root'
})
export class UserService {
    
    constructor(
        private http: HttpClient,
        private cookieService: CookieService
    ) {
  
    }
  

  
    create_user(username: string, password: string): Observable<User> {
        const body = {
          "image_path": "----",
          "description": "nice kille",
          "username": username,
          "password": password
        };
        return this.http.post<User>(environment.baseUrl+"/users/create", body);
    }

    login_user(username: string, password: string): Observable<User> {
      return this.http.get<User>(environment.baseUrl+"/users/login/"+username+":"+password);
    }

    get_me(): Observable<User> {

      let id = this.cookieService.get('_id')

      const header = {
        'Authorization': id
      };

      return this.http.get<User>(environment.baseUrl+"/users/me", { headers: header });
    }
  }
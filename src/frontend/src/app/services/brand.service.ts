import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {Beverage} from 'src/app/models/beverage.model';
import {environment} from 'src/environments/environment';
import {CookieService} from "ngx-cookie-service";

@Injectable({
  providedIn: 'root'
})
export class BrandService {

  constructor(
    private http: HttpClient,
    private cookieService: CookieService
  ) {

  }

  create_brand(name: string, description: string): Observable<string> {
    const header: { Authorization: string } = {'Authorization': `Bearer ${this.cookieService.get('token')}`}
    const body = {
      'name': `${name}`, 'description': `${description}`
    };
    return this.http.post<string>(environment.baseUrl + "/brands", body, {headers: header});
  }

  update_brand(name: string, description: string): Observable<string> {
    const header: { Authorization: string } = {'Authorization': `Bearer ${this.cookieService.get('token')}`}
    let body: any;
    if (!name && !description) {
      throw new Error("Cannot update with no changed values");
    } else if (!name) {
      body = {
        'description': `${description}`
      };
    } else if (!description) {
      body = {
        'name': `${name}`
      };
    } else {
      body = {
        'name': `${name}`, 'description': `${description}`
      };
    }
    return this.http.patch<string>(environment.baseUrl + "/brands/" + name, body, {headers: header});
  }

  delete_brand(name: string): Observable<string> {
    const header: { Authorization: string } = {'Authorization': `Bearer ${this.cookieService.get('token')}`}
    return this.http.delete<string>(environment.baseUrl + "/brands/"+name, {headers: header});
  }
}

import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {Beverage} from 'src/app/models/beverage.model';
import {environment} from 'src/environments/environment';
import {CookieService} from "ngx-cookie-service";

@Injectable({
  providedIn: 'root'
})
export class BeverageService {

  constructor(
    private http: HttpClient,
    private cookieService: CookieService
  ) {

  }

  create_beverage(name: string, description: string, image: string, bitt: number, full: number, sweet: number, abv: number, bevType: string, country: string, brand_id: string): Observable<string> {
    const header: { Authorization: string } = {'Authorization': `Bearer ${this.cookieService.get('token')}`}
    const body = {
      'name': `${name}`,
      'description': `${description}`,
      'image_path': `${image}`,
      'bitterness': `${bitt}`,
      'fullness': `${full}`,
      'sweetness': `${sweet}`,
      'abv': `${abv}`,
      'beverageType': `${bevType}`,
      'country': `${country}`,
      'brand_id': `${brand_id}`,
    };
    return this.http.post<string>(environment.baseUrl + "/beverages", body, {headers: header});
  }

  update_beverage(name: string, description: string, image: string, bitt: number, full: number, sweet: number, abv: number, bevType: string, country: string, brand_id: string): Observable<string> {
    const header: { Authorization: string } = {'Authorization': `Bearer ${this.cookieService.get('token')}`}
    let body:any = {};
    if (name) {
      body.name = name;
    }
    if (description) {
      body.description = description;
    }
    if (image) {
      body.image_path = image;
    }
    if (bitt) {
      body.bitterness = bitt;
    }
    if (full) {
      body.fullness = full;
    }
    if (sweet) {
      body.sweetness = sweet;
    }
    if (abv) {
      body.abv = abv;
    }
    if (bevType) {
      body.beverageType = bevType;
    }
    if (country) {
      body.country = country;
    }
    if (brand_id) {
      body.brand_id = brand_id;
    }
    if (body.length === 0) {
      throw new Error("Cannot update with no changed values");
    }
    return this.http.patch<string>(environment.baseUrl + "/beverages/" + name, body, {headers: header});
  }

  delete_beverage(name: string): Observable<string> {
    const header: { Authorization: string } = {'Authorization': `Bearer ${this.cookieService.get('token')}`}
    return this.http.delete<string>(environment.baseUrl + "/beverages/"+name, {headers: header});
  }

  get_all_beverages(page: number, search: string): Observable<Beverage[]> {
    return this.http.get<Beverage[]>(environment.baseUrl + "/beverages?size=15&page=" + page + "&q=" + search);
  }

  get_beverage(id: string): Observable<Beverage> {
    return this.http.get<Beverage>(environment.baseUrl + "/beverages/" + id);
  }
}

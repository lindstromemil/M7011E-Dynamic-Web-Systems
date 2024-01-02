import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {Beverage} from 'src/app/models/beverage.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn:'root'
})
export class BeverageService {

    constructor(
        private http: HttpClient,
    ) {

    }

    get_all_beverages(page: number, search: string): Observable<Beverage[]> {
      return this.http.get<Beverage[]>(environment.baseUrl+"/beverages?size=15&page="+page+"&q="+search);
    }
  }

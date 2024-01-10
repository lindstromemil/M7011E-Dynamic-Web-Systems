import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Planning } from '../models/planning.model';
import { User } from '../models/user.model';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root',
})
export class PlanningService {
  constructor(private http: HttpClient, private cookieService: CookieService) {}
  get_all_plannings(personId: string): Observable<Planning[]> {
    return this.http.get<Planning[]>(
      environment.baseUrl + '/planning?&q=' + personId
    );
  }

  create_planning(user_id: string, beverage_id: string): Observable<string> {
    const header: { Authorization: string } = {
      Authorization: `Bearer ${this.cookieService.get('token')}`,
    };
    var body = {
      user_id: user_id,
      beverage_id: beverage_id,
    };
    return this.http.post<string>(environment.baseUrl + '/planning', body, {
      headers: header,
    });
  }
}

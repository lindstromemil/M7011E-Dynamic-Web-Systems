import {HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import {Planning} from "../models/planning.model";
import {User} from "../models/user.model";

@Injectable({
  providedIn:'root'
})
export class PlanningService {

    constructor(
        private http: HttpClient,
    ) {

    }
    get_all_plannings(personId: string): Observable<Planning[]> {
      return this.http.get<Planning[]>(environment.baseUrl+"/planning?&q="+personId);
    }
  }

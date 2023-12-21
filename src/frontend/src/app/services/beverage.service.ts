import { Injectable } from "@angular/core";
import { HttpClient, HttpRequest } from "@angular/common/http";
import { Observable } from "rxjs";
import { Beverage } from "../models/beverage.model";
import { environment } from "src/environments/environment";

@Injectable({
    providedIn: 'root'
})

export class BeverageService {

    private jsonURL = 'assets/beverageExample.json';

    constructor(private http: HttpClient) { }

    getBeverages(name?: string, type?: string, brand?: string, country?: string): Observable<Beverage[]> {
        // If empty search return test data
        if (!name && !type && !brand && !country) {
            return this.http.get<Beverage[]>(this.jsonURL);
        }
        return this.http.get<Beverage[]>(this.jsonURL);
    };
}


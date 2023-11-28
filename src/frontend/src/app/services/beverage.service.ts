import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Beverage } from "../models/beverage.model";

@Injectable({
    providedIn: 'root'
})

export class BeverageService {

    private jsonURL = 'assets/beverageExample.json';

    constructor(private http: HttpClient) { }

    getBeverages(): Observable<Beverage[]> {
        return this.http.get<Beverage[]>(this.jsonURL);
    }
}


import {Beverage} from "./beverage.model";

export interface Rating {
  "_id": any,
  "user_id": any,
  "beverage_id": any,
  "score": number,
  "comment": string,
  "created_at": any,
}

export interface Activity {
  "beverage": Beverage,
  "score": number,
  "created_at": string,
}

export interface Review {
  "ratingId": string,
  "beverage": Beverage,
  "score": number,
  "comment": string,
  "likes": number,
  "created_at": string,
}

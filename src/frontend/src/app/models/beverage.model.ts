import { Brand } from "./brand.model"
import { idJson } from "./idJson.model"

export interface Beverage {
    _id: idJson
    name: string
    description: string
    image_path: string
    bitterness: number
    fullness: number
    sweetness: number
    abv: number
    beverageType: string
    country: string
    brand: Brand
}

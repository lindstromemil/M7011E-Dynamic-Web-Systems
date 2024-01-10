import {Component} from '@angular/core';
import {UserService} from "../services/user.service";
import {AuthService} from "../services/auth.service";
import {CookieService} from "ngx-cookie-service";
import {Router} from "@angular/router";
import {AdminService} from "../services/admin.service";
import {RatingsService} from "../services/ratings.service";
import {BrandService} from "../services/brand.service";
import {BeverageService} from "../services/beverage.service";

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent {
  deleteInputField: string = '';
  deleteWorked: boolean = false;

  BrandNameInputFiled: string = '';
  BrandDescriptionInputFiled: string = '';
  createBrandWorked: boolean = false;
  updateBrandWorked: boolean = false;

  BeverageNameInputFiled: string = '';
  BeverageDescriptionInputFiled: string = '';
  BeverageImageInputFiled: string = '';
  BeverageBitternessInputFiled: string = '';
  BeverageFullnessInputFiled: string = '';
  BeverageSweetnessInputFiled: string = '';
  BeverageAbvInputFiled: string = '';
  BeverageTypeInputFiled: string = '';
  BeverageCountryInputFiled: string = '';
  BeverageBrandIdInputFiled: string = '';

  createBeverageWorked: boolean = false;
  updateBeverageWorked: boolean = false;


  constructor(
    private userAPI: UserService,
    private authService: AuthService,
    private router: Router,
    private ratingAPI: RatingsService,
    private brandAPI: BrandService,
    private beverageAPI: BeverageService,
    private adminService: AdminService
  ) {
    authService.ngOnInit();
    adminService.admin_me().subscribe(
      (isAdmin: boolean) => {
        if (!isAdmin) {
          this.router.navigate(['activity']);
        }
      },
      err => {
        console.error(err.error)
      }
    )
  }

  deleteUser() {
    this.userAPI.delete_user(this.deleteInputField).subscribe(
      () => {
        this.deleteWorked = true;
      },
      err => {
        console.error(err.error)
      }
    )
  }

  deleteRating() {
    this.ratingAPI.delete_rating(this.deleteInputField).subscribe(
      () => {
        this.deleteWorked = true;
      },
      err => {
        console.error(err.error)
      }
    )
  }

  createBrand() {
    this.brandAPI.create_brand(this.BrandNameInputFiled, this.BrandDescriptionInputFiled).subscribe(
      () => {
        this.createBrandWorked = true;
      },
      err => {
        console.error(err.error)
      }
    )
  }

  updateBrand() {
    this.brandAPI.update_brand(this.BrandNameInputFiled, this.BrandDescriptionInputFiled).subscribe(
      () => {
        this.updateBrandWorked = true;
      },
      err => {
        console.error(err.error)
      }
    )
  }

  deleteBrand() {
    this.brandAPI.delete_brand(this.deleteInputField).subscribe(
      () => {
        this.deleteWorked = true;
      },
      err => {
        console.error(err.error)
      }
    )
  }

  createBeverage() {
    this.beverageAPI.create_beverage(
      this.BeverageNameInputFiled,
      this.BeverageDescriptionInputFiled,
      this.BeverageImageInputFiled,
      Number(this.BeverageBitternessInputFiled),
      Number(this.BeverageFullnessInputFiled),
      Number(this.BeverageSweetnessInputFiled),
      Number(this.BeverageAbvInputFiled),
      this.BeverageTypeInputFiled,
      this.BeverageCountryInputFiled,
      this.BeverageBrandIdInputFiled).subscribe(
      () => {
        this.createBeverageWorked = true;
      },
      err => {
        console.error(err.error)
      }
    )
  }

  updateBeverage() {
    this.beverageAPI.update_beverage(
      this.BeverageNameInputFiled,
      this.BeverageDescriptionInputFiled,
      this.BeverageImageInputFiled,
      Number(this.BeverageBitternessInputFiled),
      Number(this.BeverageFullnessInputFiled),
      Number(this.BeverageSweetnessInputFiled),
      Number(this.BeverageAbvInputFiled),
      this.BeverageTypeInputFiled,
      this.BeverageCountryInputFiled,
      this.BeverageBrandIdInputFiled).subscribe(
      () => {
        this.updateBeverageWorked = true;
      },
      err => {
        console.error(err.error)
      }
    )
  }

  deleteBeverage() {
    this.beverageAPI.delete_beverage(this.deleteInputField).subscribe(
      () => {
        this.deleteWorked = true;
      },
      err => {
        console.error(err.error)
      }
    )
  }

  goBack() {
    this.router.navigate(['activity']);
  }
}

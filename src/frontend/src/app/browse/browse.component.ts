import {Component, HostListener, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {BeverageService} from "../services/beverage.service";
import {Beverage} from "../models/beverage.model";
import {FormControl} from "@angular/forms";
import {debounceTime} from "rxjs";

@Component({
  selector: 'app-browse',
  templateUrl: './browse.component.html',
  styleUrls: ['./browse.component.css'],
})
export class BrowseComponent implements OnInit {
  beverages: Beverage[] = [];
  loading: boolean = false; // Indicates if new data is being loaded
  currentPage: number = 1; // Track the current page
  searchInput: FormControl = new FormControl();
  data: any = {};

  constructor(
    private router: Router,
    private beverageAPI: BeverageService,
  ) {
  }

  ngOnInit() {
    this.load_more_content(1, "");
    this.searchInput.valueChanges
    .pipe(
      debounceTime(300)
      )
      .subscribe(() => {
        this.load_search(this.searchInput.value);
      });
  }

  @HostListener('window:scroll', ['$event'])
  onScroll(event: Event): void {

  // Check if the user has reached the exact bottom of the page
  if (document.documentElement.clientHeight + window.scrollY >=(document.documentElement.scrollHeight || document.documentElement.clientHeight)) {
      this.currentPage++;
      this.load_more_content(this.currentPage, this.searchInput.value);
    }
  }

  load_more_content(page: number, search: string) {
    if (!search) {
      search = "";
    }
    console.log("load more content");
    console.log(page);
    console.log(search);
    this.loading = true;
    this.beverageAPI.get_all_beverages(page, search).subscribe(
        (beverages: Beverage[]) => {

          this.beverages = [...this.beverages, ...beverages];
        },
        err => {
          console.error(err.error)
        }
      )
    this.loading = false;
  }

  load_search(searchQuery : string) {
    this.loading = true;
    this.currentPage = 1;
    this.beverageAPI.get_all_beverages(1, searchQuery).subscribe(
        (beverages: Beverage[]) => {
          this.beverages = beverages;
        },
        err => {
          console.error(err.error)
        }
      )
    this.loading = false;
  }

  round(value: number, precision: number) {
    var multiplier = Math.pow(10, precision.valueOf() || 0);
    return Math.round(value.valueOf() * multiplier) / multiplier;
  }
  convertToPercentage(str: number): number {
    const percentage = str * 100;
    return this.round(percentage, 1);
  }

  navigateToBeveragePage(name: string) {
    console.log(name);
    this.router.navigate(['entry']);
  }
}

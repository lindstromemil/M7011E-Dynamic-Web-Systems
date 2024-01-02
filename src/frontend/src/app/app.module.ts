import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { AdminComponent } from './admin/admin.component';
import { BrowseComponent } from './browse/browse.component';
import { IndividualEntriesComponent } from './individual-entries/individual-entries.component';
import { BreweryComponent } from './brewery/brewery.component';
import { ActivityComponent } from './activity/activity.component';
import { ProfileComponent } from './profile/profile.component';
import { UserService} from './services/user.service'
import { NavbarComponent } from './navbar/navbar.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import {SettingsComponent} from "./settings/settings.component";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {MatInputModule} from "@angular/material/input";

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    AdminComponent,
    BrowseComponent,
    IndividualEntriesComponent,
    BreweryComponent,
    ActivityComponent,
    ProfileComponent,
    NavbarComponent,
    SettingsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatButtonModule,
    FormsModule,
    MatProgressSpinnerModule,
    MatInputModule,
    ReactiveFormsModule
  ],
  providers: [CookieService, UserService],
  bootstrap: [AppComponent]
})
export class AppModule { }

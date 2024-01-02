import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { AdminComponent } from './admin/admin.component';
import { BrowseComponent } from './browse/browse.component';
import { IndividualEntriesComponent } from './individual-entries/individual-entries.component';
import { BreweryComponent } from './brewery/brewery.component';
import { ActivityComponent } from './activity/activity.component';
import { ProfileComponent } from './profile/profile.component';
import {SettingsComponent} from "./settings/settings.component";
import {ListComponent} from "./list/list.component";
import {SocialComponent} from "./social/social.component";
import {ReviewsComponent} from "./reviews/reviews.component";

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'admin', component: AdminComponent },
  { path: 'browse', component: BrowseComponent },
  { path: 'entry', component: IndividualEntriesComponent },
  { path: 'brewery', component: BreweryComponent },
  { path: 'activity', component: ActivityComponent },
  { path: 'user/:username', component: ProfileComponent },
  { path: 'user/:username/list', component: ListComponent },
  { path: 'user/:username/social', component: SocialComponent },
  { path: 'user/:username/reviews', component: ReviewsComponent },
  { path: 'settings', component: SettingsComponent },
  { path: '**', component: LoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

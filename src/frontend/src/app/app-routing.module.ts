import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './components/login/login.component';
import { AdminComponent } from './components/admin/admin.component';
import { BrowseComponent } from './components/browse/browse.component';
import { IndividualEntriesComponent } from './components/individual-entries/individual-entries.component';
import { BreweryComponent } from './components/brewery/brewery.component';
import { ActivityComponent } from './components/activity/activity.component';
import { ProfileComponent } from './components/profile/profile.component';

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'admin', component: AdminComponent },
  { path: 'browse', component: BrowseComponent },
  { path: 'beverage/:id', component: IndividualEntriesComponent },
  { path: 'brewery', component: BreweryComponent },
  { path: 'activity', component: ActivityComponent },
  { path: 'profile', component: ProfileComponent },
  { path: '**', component: LoginComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

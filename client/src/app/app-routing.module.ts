import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from "./login/login.component";
import { LibrarianViewComponent } from "./librarian-view/librarian-view.component";
import { LibrarianGuardService } from "./librarian-guard.service";

const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: LoginComponent,
    data: { state: 'login' }
  },
  {
    path: 'admin',
    component: LibrarianViewComponent,
    canActivate: [LibrarianGuardService],
    data: { state: 'admin' }
  }
];

@NgModule({
  exports: [
    RouterModule
  ],
  imports: [
    RouterModule.forRoot(routes)
  ]
})
export class AppRoutingModule { }

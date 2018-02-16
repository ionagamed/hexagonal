import { Injectable } from '@angular/core';
import { AuthService } from "./auth.service";
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot } from "@angular/router";
import { Observable } from "rxjs/Observable";

@Injectable()
export class LibrarianGuardService implements CanActivate {

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {
    return this.auth.role == 'librarian';
  }

  constructor(private auth: AuthService) { }

}

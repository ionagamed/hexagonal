import { Injectable } from '@angular/core';
import { JsonrpcService } from "./jsonrpc.service";
import { map } from "rxjs/operators";
import "rxjs/add/operator/mergeMap";

@Injectable()
export class AuthService {

  public login: string;
  public role: string;

  constructor(private rpc: JsonrpcService) {
  }

  authenticate(login: string, password: string) {
    return this.rpc.call('auth.login', [login, password]).flatMap(x => {
      this.rpc.token = x;
      this.login = login;
      return this.rpc.call('auth.get_my_role', []).pipe(
        map(x => {
          this.role = x;
          console.log(x);
          return x;
        })
      );
    });
  }

}

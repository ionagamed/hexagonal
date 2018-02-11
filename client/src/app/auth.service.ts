import { Injectable } from '@angular/core';
import {JsonrpcService} from "./jsonrpc.service";

@Injectable()
export class AuthService {

  private login: string;
  private role: string;

  constructor(private rpc: JsonrpcService) { }

  authenticate(login: string, password: string) {
    this.rpc.call('auth.login', [login, password]).subscribe(x => {
      this.rpc.token = x;
      this.login = login;
      this.rpc.call('auth.get_my_role', []).subscribe(x => this.role = x)
    });

  }

}

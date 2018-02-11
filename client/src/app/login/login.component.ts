import { Component, OnInit } from '@angular/core';
import {JsonrpcService} from "../jsonrpc.service";
import {AuthService} from "../auth.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private rpc: JsonrpcService, private auth: AuthService) { }

  login: string;
  password: string;

  ngOnInit() {

  }

  authenticate() {
    console.log(this.login);
    console.log(this.password);
    this.auth.authenticate(this.login, this.password);
  }

}

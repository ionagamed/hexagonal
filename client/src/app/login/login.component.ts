import { Component, OnInit } from '@angular/core';
import { JsonrpcService } from "../jsonrpc.service";
import { AuthService } from "../auth.service";
import { Router } from "@angular/router";
import 'rxjs/add/operator/delay'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private rpc: JsonrpcService, private auth: AuthService, private router: Router) { }

  login: string;
  password: string;

  loading: boolean = false;

  ngOnInit() {
    this.login = 'root';
    this.password = 'toor';
    this.authenticate();
  }

  authenticate() {
    this.loading = true;
    this.auth.authenticate(this.login, this.password).delay(1000).subscribe((x) => {
      this.router.navigate(['/admin'])
    });
  }

}

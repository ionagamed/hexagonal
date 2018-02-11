import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { environment } from '../environments/environment';
import { map } from "rxjs/operators";

@Injectable()
export class JsonrpcService {

  public token: string;

  constructor(private http: HttpClient) { }

  call(method: String, args: Object) {
    let headers = {
      'Content-Type': 'application/json'
    };
    if (this.token) {
      headers['Authorization'] = this.token
    }
    return this.http.post(environment.rpcEndpoint, {
      jsonrpc: '2.0',
      method: method,
      params: args
    }, {
      headers: headers
    }).pipe(map(x => x['result']))
  }

}

import { Injectable } from '@angular/core';
import { JsonrpcService } from "../jsonrpc.service";
import { Observable } from "rxjs/Observable";
import { Document } from "./document";
import { map } from "rxjs/operators";

@Injectable()
export class DocumentService {

  constructor(private rpc: JsonrpcService) { }

  getAllDocuments(): Observable<Document[]> {
    return this.rpc.call('document.get', []).pipe(map(x => {
      let docs = [];
      for (let i of x) {
        docs.push(new Document(i.id, i.title));
      }
      return docs
    }));
  }

}

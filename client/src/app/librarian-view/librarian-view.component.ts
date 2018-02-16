import { Component, OnInit } from '@angular/core';
import { DocumentService } from "../document/document.service";
import { Document } from "../document/document";
import { $ } from "protractor";

@Component({
  selector: 'app-librarian-view',
  templateUrl: './librarian-view.component.html',
  styleUrls: ['./librarian-view.component.css']
})
export class LibrarianViewComponent implements OnInit {

  constructor(private ds: DocumentService) { }

  docs: Array<Document> = [];

  ngOnInit() {
    this.ds.getAllDocuments().subscribe(x => {
      this.docs = x;
    });
  }
}

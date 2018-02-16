import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { AuthService } from './auth.service';
import { HttpClientModule } from "@angular/common/http";
import { JsonrpcService } from "./jsonrpc.service";
import { FormsModule } from "@angular/forms";
import { AppRoutingModule } from './app-routing.module';
import { LibrarianViewComponent } from './librarian-view/librarian-view.component';
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { LibrarianGuardService } from "./librarian-guard.service";
import { DocumentService } from "./document/document.service";


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    LibrarianViewComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    AppRoutingModule
  ],
  providers: [
    AuthService,
    JsonrpcService,
    LibrarianGuardService,
    DocumentService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}

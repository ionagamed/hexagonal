import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { AuthService } from './auth.service';
import { HttpClientModule } from "@angular/common/http";
import {JsonrpcService} from "./jsonrpc.service";
import {FormsModule} from "@angular/forms";


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    AuthService,
    JsonrpcService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

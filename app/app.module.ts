import './rxjs-extensions';

import { HttpModule }    from '@angular/http';

import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent }   from './app.component';

import { HTTPReq }          from './httpReq.service';

@NgModule({
  imports:      [
	  BrowserModule,
	  HttpModule
   ],
  declarations: [ AppComponent ],
  bootstrap:    [ AppComponent ],
  providers: [
    HTTPReq
  ]
})
export class AppModule { }

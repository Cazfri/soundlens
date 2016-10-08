import { Component } from '@angular/core';

import { HTTPReq } from './httpReq.service';

@Component({
  selector: 'my-app',
  template: '<h1>My Second Angular App</h1>',
  providers: [HTTPReq]
})
export class AppComponent {
	constructor(private httpReq: HTTPReq) { }
}

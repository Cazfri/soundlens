import { Injectable } from '@angular/core';
import { Headers, Http, Response } from '@angular/http';
import { Observable } from 'rxjs';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class HTTPReq {
	constructor(private http: Http) { }

	req() {
		return this.http.get('app/getInfo')
               .toPromise()
               .then((response) => {
				  console.log(response.json().data);
			   })
               .catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
   		console.error('An error occurred', error); // for demo purposes only
   		return Promise.reject(error.message || error);
 	}
}

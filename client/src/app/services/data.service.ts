import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  url1 = "http://localhost:4000/api/list/";
  url2 = "http://localhost:4000/api/dashboard/";

  constructor(private http: HttpClient) { }

  getEmployees(token: string): Observable<any> {
    return this.http.post<any>(this.url1, { token: token });
  }
  
  getEmployee(token: string): Observable<any> {
    return this.http.post<any>(this.url2, { token: token });
  }
}

import { Component, OnInit } from '@angular/core';
import { Observable , Subject} from 'rxjs';
import { Employee } from 'src/app/employee';
import { DataService } from 'src/app/services/data.service';
import { HttpClient } from '@angular/common/http';

declare var $: any;


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  isAuthenticated : string = "false";
  employees:Employee[]=[];
  token:string='';
  name: string='';
  temp:string|null='';
  role:string='';
  constructor(private dataService: DataService,private http:HttpClient) { }
  dtOptions: DataTables.Settings = {};
  dtTrigger: Subject<any> = new Subject<any>();
  


  ngOnInit(): void {

    $(document).ready(() => {
      $('#carouselExampleIndicators').carousel();
    });
  
    this.temp=localStorage.getItem('token');
      if(this.temp!=null){
        this.token=this.temp;
      }
      this.getEmployeesList().subscribe((data1) => {
          this.employees=data1['employees'];
          this.dtTrigger.next(null);
          // console.log(data1['isAuthenticated']);
          if(data1['isAuthenticated']=="true"){this.isAuthenticated="true";}});
      this.getRole();
      this.setRole();
      this.getName();
      this.setName();

      this.dtOptions = {
        pagingType:'full_numbers',
        searching:true,
        ordering: false,
        language: {
          searchPlaceholder: "Search...",
          search: ""
        },       
      };
  }

  getEmployeesList():Observable<any>{
    return this.dataService.getEmployees(this.token);
}
  logout(){
    localStorage.removeItem('token');
    this.isAuthenticated="false";
    window.location.reload();
  }
  getRole():Observable<any>{
    const url="http://localhost:4000/api/role/";
    return this.http.post(url,{token:this.token});
  }
  setRole(){
    this.getRole().subscribe((data1) => {
      this.role=data1['role'];
    });
  }

  getName():Observable<any>{
    const url2="http://localhost:4000/api/dashboard/";
    return this.http.post(url2,{token:this.token});
  }
  setName(){
    this.getName().subscribe((data2) => {
      console.log(data2);
      console.log("hellooo");
      this.name=data2.employee.name;   
    });
  }

  
}

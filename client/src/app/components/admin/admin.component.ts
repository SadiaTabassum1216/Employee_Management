import { Component, OnInit } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { Employee } from 'src/app/employee';
import { DataService } from 'src/app/services/data.service';
import { HttpClient } from '@angular/common/http';
import * as crypto from 'crypto-js';
import { NgbModalConfig, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent {
  isAuthenticated : string = "false";
  employees:Employee[]=[];
  update :boolean=false;
  create: boolean=false;
  token:string='';
  temp:string|null='';
  role:string='';
  selectedEmployee : Employee =new Employee('','','','','','','','');
  newEmployee : Employee =new Employee('','','','','','','','');

  dtOptions: DataTables.Settings = {};
  dtTrigger: Subject<any> = new Subject<any>();

  constructor(private dataService: DataService,private http:HttpClient,
     config: NgbModalConfig, private modalService: NgbModal, private toastr: ToastrService) { 
    config.backdrop = 'static';
		config.keyboard = false;
  }

  ngOnInit(): void {
   
    this.temp=localStorage.getItem('token');
      if(this.temp!=null){
        this.token=this.temp;
      }
      this.getRole();
      this.setRole();

      this.dtOptions = {
        pagingType:'full_numbers',
        searching:true,
        ordering: false,
        language: {
          searchPlaceholder: "Search...",
          search: ""
        },
       
      };
      
      this.getEmployeesList().subscribe((data1) => {
          this.employees=data1['employees'];          
           this.dtTrigger.next(null);
          console.log(data1);});
      
  }

  
  

  getEmployeesList():Observable<any>{
    return this.dataService.getEmployees(this.token);
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

  updateEmployee():Observable<any>{
    const url="http://localhost:4000/api/editEmployee/";
    return this.http.post(url,{token:this.token,id:this.selectedEmployee.id,designation:this.selectedEmployee.designation,department:this.selectedEmployee.department,salary:this.selectedEmployee.salary});
  }
  createdEmployee():Observable<any>{
    const url="http://localhost:4000/api/addEmployee/";
    let hash = crypto.SHA256(this.newEmployee.password).toString();
    return this.http.post(url,{token:this.token,name:this.newEmployee.name,password:hash,id:this.newEmployee.id,designation:this.newEmployee.designation,department:this.newEmployee.department,salary:this.newEmployee.salary});
  }
  createEmployee(){
    this.createdEmployee().subscribe((data1)=>{
      this.toastr
      .success("Success",data1['message'], { closeButton: true })
      .onTap.subscribe((action) =>window.location.reload())
   
    });}
  removeEmployee(employee:Employee){
    this.deleteEmployee(employee).subscribe((data1)=>{
      this.toastr
      .success("Success",data1['message'], { closeButton: true })
      .onTap.subscribe((action) =>window.location.reload())
    });

  }
  updatedEmployee(){
    this.updateEmployee().subscribe((data1)=>{
      this.toastr.success(data1['message'])

    });}
  deleteEmployee(employee:Employee):Observable<any>{
    const url="http://localhost:4000/api/removeEmployee/";
    return this.http.post(url,{token:this.token,id:employee.id});
  }
  selectEmployee(employee:Employee){
    this.update=true;
    this.selectedEmployee=employee;
  }
  logout(){
    localStorage.removeItem('token');
    this.isAuthenticated="false";
    window.location.reload();
  }

  open(content: any) {
		this.modalService.open(content);
	}

}

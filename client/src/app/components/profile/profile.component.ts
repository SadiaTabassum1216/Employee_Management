import { Component, OnInit ,ViewChild} from '@angular/core';
import { Observable } from 'rxjs';
import { Employee } from 'src/app/employee';
import { DataService } from 'src/app/services/data.service';
import { HttpClient } from '@angular/common/http';
import * as crypto from 'crypto-js';
import { NgbModalConfig,NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'],
})
export class ProfileComponent {
 
  isAuthenticated : string = "false";
  updatePass :boolean=false;
  updateContact: boolean=false;
  token:string='';
  temp:string|null='';
  role:string='';
  selectedEmployee : Employee =new Employee('','','','','','','','');
  constructor(private dataService: DataService,private http:HttpClient,config: NgbModalConfig, private modalService: NgbModal, private toastr: ToastrService) {
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
      this.getEmployee().subscribe((data1) => {
          this.selectedEmployee=data1['employee'];});
      
  }

  getEmployee():Observable<any>{
    return this.dataService.getEmployee(this.token);
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

  updatedPassword(): Observable<any> {
    const url = "http://localhost:4000/api/editPassword/";
    let hash = crypto.SHA256(this.selectedEmployee.password).toString();
    return this.http.post(url, { token: this.token, password: hash });
  }

  updatePassword() {
    this.updatedPassword().subscribe((data1) => {
      this.toastr.success(data1['message']);
    });
  }

  changePassword(){
  this.updatePass=true;
 
   
  }
  changeInfo(){
    this.updateContact=true;
  }
  updatedInfo(): Observable<any> {
    const url = "http://localhost:4000/api/editProfile/";
    return this.http.post(url, { token: this.token, address: this.selectedEmployee.address, phone: this.selectedEmployee.phone, email:this.selectedEmployee.email });
  }

  updateInfo() {
    this.updatedInfo().subscribe((data1) => {
      this.toastr.success(data1['message']);
   //   window.location.reload();
    });
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

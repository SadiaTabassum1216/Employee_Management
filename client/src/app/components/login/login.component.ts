import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import * as crypto from 'crypto-js';
import { DataService } from 'src/app/services/data.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],

})
export class LoginComponent {
  isAuthenticated : boolean = false;
  token:string='';
  temp:string|null='';
  
  signInForm: FormGroup;
  url:string="http://localhost:4000/api/login/";
  constructor(private dataService: DataService,private http:HttpClient, private router:Router,private fb: FormBuilder, private toastr: ToastrService) {
    this.signInForm = this.fb.group({
      loginID: ['', Validators.required],
      password: ['', Validators.required]
    });
}
  
  ngOnInit(): void {
    this.temp=localStorage.getItem('token');
      if(this.temp!=null){
        this.token=this.temp;
      }
      this.check().subscribe((data1) => {
        if(data1['isAuthenticated']=="true"){this.isAuthenticated=true;
          this.toastr.info('Already Logged In');
        this.router.navigate(['/home']);}});
    }

  check():Observable<any>{
    return this.http.post(this.url,{token:this.token,password:'',id:''});
  }
  login(){
    this.match().subscribe((data1) => {
      if(data1['message']==='Login Successful')
        {this.toastr.success(data1['message']);}
        else{
          this.toastr.error(data1['message']);
        }
      
      if(data1['isAuthenticated']=="true"){this.isAuthenticated=true;
        localStorage.setItem('token',data1['token']);
        this.router.navigate(['/home']);
      }});

  }
  match():Observable<any>{
    let hash = crypto.SHA256(this.signInForm.get('password')?.value).toString();
    return this.http.post(this.url,{token:this.token,password:hash,id:this.signInForm.get('loginID')?.value});}

}



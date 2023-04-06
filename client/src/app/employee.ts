export class Employee{
    name: string;
    id: string;
    designation: string;
    department:string;
    phone: string;
    email: string;
    address: string;
    salary:string;
    password:string;
    
  
    constructor(name: string, id: string, designation: string, department: string, phone: string, email: string, address: string, salary: string) {
        this.name = name;
        this.id = id;
        this.designation = designation;
        this.department = department;
        this.phone = phone;
        this.email = email;
        this.address = address;
        this.salary = salary;
        this.password='';
        this.address=address;
      }
    
  }
import json
import jwt
from django.conf import settings
from django.db import connection

class employee:
    def __init__(self,id,name,phone,email,address,designation,department,salary):
       self.id=id
       self.name=name
       self.phone=phone
       self.email=email
       self.address=address
       self.salary=salary
       self.designation=designation
       self.department=department

def updateInfo(request):
    req=json.load(request)
    token=req['token']

    try:
        # Decode the JWT using the secret key
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        result = {'id':decoded_jwt['id'],'role':decoded_jwt['role'], 'isAuthenticated' : 'true'}
        id=decoded_jwt['id']
        if(result['role']=='employee'):
            sql_query = f"SELECT * FROM accounts WHERE id='{decoded_jwt['id']}';"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()

            if(len(rows)==0):
                return {'message' : 'Employee does not exist anymore','isAuthenticated' : 'false'}
            sql_query = f"UPDATE accounts SET phone='{req['phone']}',email='{req['email']}',address='{req['address']}' where id='{id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

            return  {'message' : 'Employee successfully updated','isAuthenticated' : 'true'}
        
        else:    
            return {'message' : 'Needs employee permissions','isAuthenticated' : 'false'}
    except jwt.exceptions.DecodeError:
        # Return None if the JWT is invalid
        return {'message' : 'Needs employee permissions','isAuthenticated' : 'false'}
    
def updatePassword(request):
    req=json.load(request)
    token=req['token']

    try:
        # Decode the JWT using the secret key
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        result = {'id':decoded_jwt['id'],'role':decoded_jwt['role'], 'isAuthenticated' : 'true'}
        id=decoded_jwt['id']
        if(result['role']=='employee'):
            sql_query = f"SELECT * FROM accounts WHERE id='{decoded_jwt['id']}';"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()

            if(len(rows)==0):
                return {'message' : 'Employee does not exist anymore','isAuthenticated' : 'false'}
            
            sql_query = f"UPDATE accounts SET password='{req['password']}' where id='{id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

            return  {'message' : 'Password successfully updated','isAuthenticated' : 'true'}
        
        else:    
            return {'message' : 'Needs employee permissions','isAuthenticated' : 'false'}
    except jwt.exceptions.DecodeError:
        # Return None if the JWT is invalid
        return {'message' : 'Needs employee permissions','isAuthenticated' : 'false'}
    
def getProfile(request):
    req=json.load(request)
    token=req['token']

    try:
        # Decode the JWT using the secret key
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        isAuthenticated='true'
        sql_query = f"SELECT * FROM accounts WHERE id='{decoded_jwt['id']}';"
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()

        if(len(rows)==0):
            return {'message' : 'Employee does not exist anymore','isAuthenticated' : 'false'}

        sql_query = f"SELECT * FROM employees WHERE id='{decoded_jwt['id']}';"
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows1 = cursor.fetchall()

        row=rows[0]
        row1=rows1[0]

        obj=employee(row[0],row1[1],row[3],row[4],row[5],row1[2],row1[3],row1[4])
        return {'employee' : obj.__dict__,'isAuthenticated' : 'true'}


    except jwt.exceptions.DecodeError:
        # Return None if the JWT is invalid
        return {'message' : 'Needs employee permissions','isAuthenticated' : 'false'}
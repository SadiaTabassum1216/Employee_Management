
import json
import jwt
from django.conf import settings
from django.db import connection



def addEmployee(request):
    req=json.load(request)
    id=req['id']
    token=req['token']

    try:
        # Decode the JWT using the secret key
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        result = {'id':decoded_jwt['id'], 'isAuthenticated' : 'true'}
        if(result['id']=='admin'):
            sql_query = f"SELECT id FROM employees where id='{id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()

            if len(rows) == 1:
                message = "Employee is already registered"
                return {'message' : 'Employee is already registered','isAuthenticated' : 'false'}

            sql_query = f"INSERT INTO employees values('{req['id']}','{req['name']}','{req['designation']}','{req['department']}',{req['salary']});"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

            sql_query = f"INSERT INTO accounts values('{req['id']}','{req['password']}','employee',Null,Null,Null);"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
            return  {'message' : 'Employee successfully registered','isAuthenticated' : 'true'}
        
        else:    
            return {'message' : 'Needs admin permissions','isAuthenticated' : 'false'}
    except jwt.exceptions.DecodeError:
        # Return None if the JWT is invalid
        return {'message' : 'Needs admin permissions','isAuthenticated' : 'false'}


def updateEmployee(request):
    req=json.load(request)
    id=req['id']
    token=req['token']

    try:
        # Decode the JWT using the secret key
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        result = {'id':decoded_jwt['id'], 'isAuthenticated' : 'true'}
        if(result['id']=='admin'):
            sql_query = f"UPDATE employees SET designation='{req['designation']}',department='{req['department']}',salary='{req['salary']}' where id='{id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

            return  {'message' : 'Employee successfully updated','isAuthenticated' : 'true'}
        
        else:    
            return {'message' : 'Needs admin permissions','isAuthenticated' : 'false'}
    except jwt.exceptions.DecodeError:
        # Return None if the JWT is invalid
        return {'message' : 'Needs admin permissions','isAuthenticated' : 'false'}
    

def deleteEmployee(request):
    req=json.load(request)
    id=req['id']
    token=req['token']

    try:
        # Decode the JWT using the secret key
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        result = {'id':decoded_jwt['id'], 'isAuthenticated' : 'true'}
        if(result['id']=='admin'):
            sql_query = f"DELETE FROM employees where id='{id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

            sql_query = f"DELETE FROM accounts where id='{id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

            return  {'message' : 'Employee successfully removed','isAuthenticated' : 'true'}
        
        else:    
            return {'message' : 'Needs admin permissions','isAuthenticated' : 'false'}
    except jwt.exceptions.DecodeError:
        # Return None if the JWT is invalid
        return {'message' : 'Needs admin permissions','isAuthenticated' : 'false'}
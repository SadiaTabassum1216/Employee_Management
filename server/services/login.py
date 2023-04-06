
import json
from django.db import connection
import jwt
from django.conf import settings
from rest_framework.response import Response


def login(request):
    req=json.load(request)
    token=req['token']

    try:
        # Decode the JWT using the secret key
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        isAuthenticated='true'
        message="Already Logged In"
        data = {'message': message,'isAuthenticated':isAuthenticated}
        return data
        
    except jwt.exceptions.DecodeError:
        # Return None if the JWT is invalid
        isAuthenticated='false'
        password=req['password']
        id=req['id']
        sql_query = f"SELECT id,password,role FROM accounts where id='{id}';"
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
        
        if len(rows) == 0:
            message="Employee is not registered"
            isAuthenticated='false'
            data = {'message': message,'isAuthenticated':isAuthenticated}
            return data

        
        row=rows[0]
        role=row[2]
        if password==row[1]:
            message="Login Successful"
            payload = {'id': id,'role':role}
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            isAuthenticated='true'
            data = {'message': message, 'token': token,'isAuthenticated':isAuthenticated}
            
            return data
        else:
            message="Password does not match"
            isAuthenticated='false'
            data = {'message': message,'isAuthenticated':isAuthenticated}
            return data
 
def roleManage(request):
    req=json.load(request)
    token=req['token']

    try:
        # Decode the JWT using the secret key
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        isAuthenticated='true'
        role=decoded_jwt['role']
        data = {'role': role,'isAuthenticated':isAuthenticated}
        return data
        
    except jwt.exceptions.DecodeError:
        isAuthenticated='false'
        role='None'
        data = {'role': role,'isAuthenticated':isAuthenticated}
        return data
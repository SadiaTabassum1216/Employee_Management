import requests
import json
from django.db import connection
import jwt
from django.conf import settings

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


def getEmployeeList(request):
    req=json.load(request)
    token=req['token']

    try:
        # Decode the JWT using the secret key
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        isAuthenticated='true'
        
    except jwt.exceptions.DecodeError:
        # Return None if the JWT is invalid
        isAuthenticated='false'

    sql_query = f"SELECT * FROM accounts;"
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

    sql_query = f"SELECT * FROM employees;"
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows1 = cursor.fetchall()

    employees=[]
    for row in rows:
        for row1 in rows1:
            if(row[0]==row1[0]):
                obj=employee(row[0],row1[1],row[3],row[4],row[5],row1[2],row1[3],row1[4])
                employees.append(obj.__dict__)

    return {'employees':employees,'isAuthenticated':isAuthenticated}

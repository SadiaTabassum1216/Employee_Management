import sys
import os
from django.shortcuts import render

sys.path.append("..")

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from services.list import *
from services.login import *
from services.admins import *
from services.employee import *

@api_view(['POST'])
def getList(request):
    return JsonResponse(data=getEmployeeList(request),safe=False)

@api_view(['POST'])
def signin(request):
    return JsonResponse(data=login(request))

@api_view(['POST'])
def createEmployee(request):
    return JsonResponse(data=addEmployee(request),safe=False)

@api_view(['POST'])
def editEmployee(request):
    return JsonResponse(data=updateEmployee(request),safe=False)

@api_view(['POST'])
def removeEmployee(request):
    return JsonResponse(data=deleteEmployee(request),safe=False)

@api_view(['POST'])
def editInfo(request):
    return JsonResponse(data=updateInfo(request),safe=False)

@api_view(['POST'])
def editPassword(request):
    return JsonResponse(data=updatePassword(request),safe=False)

@api_view(['POST'])
def profile(request):
    return JsonResponse(data=getProfile(request),safe=False)

@api_view(['POST'])
def role(request):
    return JsonResponse(data=roleManage(request),safe=False)

from django.urls import path
from .views import *

urlpatterns = [
    path('list/', getList),
    path('login/', signin),
    path('addEmployee/', createEmployee),
    path('editEmployee/', editEmployee),
    path('removeEmployee/', removeEmployee),
    path('dashboard/', profile),
    path('editProfile/', editInfo),
    path('editPassword/', editPassword),
    path('role/',role)]
from django.urls import path
from .views import admin_dashboard, home, patient_add, patient_details, patient_list, patient_update, patient_delete, patient_dashboard
from .views import service_create, service_list, service_update, service_delete, bill_create,bill_delete,bill_list,bill_update
from .views import patient_login, admin_login, logout_view
from .views import get_patients_by_service_and_date,get_patient_by_id,get_patients_by_name, change_patient_password

urlpatterns = [
    path('',home,name = "home"),
    path('patients/dashboard/<str:pk>',patient_dashboard, name='patient_dashboard'),
    path('patients/',patient_list,name="patients_list"),
    path('patients/details/<str:pk>', patient_details, name='patient_details'),
    path('patients/add/',patient_add, name='patient_add'),
    path('patients/update/<str:pk>/', patient_update, name='patient_update'),
    path('patients/delete/<str:pk>/', patient_delete, name='patient_delete'),
    path('services/', service_list, name='service_list'),
    path('services/new/', service_create, name='service_create'),
    path('services/edit/<int:pk>/', service_update, name='service_update'),
    path('services/delete/<int:pk>/', service_delete, name='service_delete'),
    path('bills/', bill_list, name='bill_list'),
    path('bills/new/', bill_create, name='bill_create'),
    path('bills/edit/<int:pk>/', bill_update, name='bill_update'),
    path('bills/delete/<int:pk>/', bill_delete, name='bill_delete'),
    path("patient/login/", patient_login, name="patient_login"),
    path("login/", admin_login, name="admin_login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", admin_dashboard, name="admin_dashboard"),
    path("patient/dashboard/<str:pk>", patient_dashboard, name="patient_dashboard"),
    path("patients/change-password/<str:pk>/", change_patient_password, name="change_patient_password"),
    path("patient-by-id",get_patient_by_id,name="patient_by_id"),
     path('patients-by-service/', get_patients_by_service_and_date, name='patients_by_service'),
     path('patients-by-name/',get_patients_by_name,name="patients_by_name"),
     
]
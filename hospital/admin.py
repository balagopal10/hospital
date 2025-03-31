from django.contrib import admin
from .models import Patient, Service, Bill
# Register your models here.
admin.site.register(Patient)
admin.site.register(Service)
admin.site.register(Bill)
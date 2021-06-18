from django.contrib import admin

# Register your models here.

from .models import Doctor ,Contact , Appointments

admin.site.register(Doctor)
admin.site.register(Contact)
admin.site.register(Appointments)

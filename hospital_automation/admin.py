from django.contrib import admin
from hospital_automation.models import User_type, Patient, Patient_history, Helpers_nurses, Medicines
# Register your models here.
admin.site.register(User_type)
admin.site.register(Patient)
admin.site.register(Patient_history)
admin.site.register(Helpers_nurses)
admin.site.register(Medicines)

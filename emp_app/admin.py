from django.contrib import admin
from .models import Employee, Department, Position,LeaveRequest


# Register models in admin
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(LeaveRequest)


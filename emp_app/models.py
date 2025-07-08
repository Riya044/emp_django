from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser, BaseUserManager



class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    employee_id = models.CharField(max_length=10, unique=True, blank=True)  # Auto-generated
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    employment_type = models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time')],default='Full-time')
    
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # Generate employee_id only if it's not already set
        if not self.employee_id:
            last_employee = Employee.objects.all().order_by('id').last()
            if last_employee:
                last_id = int(last_employee.employee_id.replace('EMP', ''))
                new_id = f'EMP{last_id + 1:03d}'
            else:
                new_id = 'EMP001'
            self.employee_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.name} ({self.position})"



class LeaveRequest(models.Model):
    """
    Represents a leave request submitted by an employee.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests',
                                 help_text="The employee submitting this leave request.")
    start_date = models.DateField()
    end_date = models.DateField()
    
    leave_type = models.CharField(max_length=50, default='Casual Leave',
                                  choices=[
                                      ('sick', 'Sick Leave'),
                                      ('casual', 'Casual Leave'),
                                      ('annual', 'Annual Leave'),
                                      ('maternity', 'Maternity Leave'),
                                      ('paternity', 'Paternity Leave'),
                                      
                                  ],
                                  help_text="Type of leave being requested.")
    status = models.CharField(max_length=20, default='Pending',
                              choices=[
                                  ('Pending', 'Pending'),
                                  ('Approved', 'Approved'),
                                  ('Rejected', 'Rejected'),
                              ],
                              help_text="Current status of the leave request.")
    requested_at = models.DateTimeField(auto_now_add=True,
                                        help_text="Timestamp when the leave request was submitted.")

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type} ({self.status})"

    class Meta:
       
        ordering = ['-start_date']




from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, LeaveRequest

from django.contrib.auth.forms import AuthenticationForm




class EmployeeRegisterForm(forms.Form):
    employee_id = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
class EmployeeLoginForm(AuthenticationForm):
    employee_id = forms.CharField(label="Employee ID")
    password = forms.CharField(widget=forms.PasswordInput)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name','email','phone','gender','department','position', 'employment_type', 'salary', 'hire_date','is_active']




class CustomAuthenticationForm(AuthenticationForm):
    
    pass

class LeaveRequestForm(forms.ModelForm):
    
   
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="End Date"
    )
    
    leave_type = forms.ChoiceField(
        choices=[
            ('', 'Select Leave Type'), 
            ('sick', 'Sick Leave'),
            ('casual', 'Casual Leave'),
            ('annual', 'Annual Leave'),
            ('maternity', 'Maternity Leave'),
            ('paternity', 'Paternity Leave'),
            
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Leave Type"
    )

    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'leave_type']
      
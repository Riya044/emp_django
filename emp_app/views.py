from django.shortcuts import render, redirect,get_object_or_404,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .forms import EmployeeRegisterForm,CustomAuthenticationForm,LeaveRequestForm,EmployeeLoginForm,EmployeeForm
from .models import Employee, LeaveRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password



def home(request):
    return render(request,'home.html')



def employee_register(request):
    if request.method == 'POST':
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            password = form.cleaned_data['password']
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                if employee.password:
                    messages.error(request, "Employee already registered.")
                else:
                    employee.password = make_password(password)
                    employee.save()
                    messages.success(request, "Registration successful! Please login.")
                    return redirect('employee_profile_dashboard')
            except Employee.DoesNotExist:
                messages.error(request, "Invalid Employee ID.")
    else:
        form = EmployeeRegisterForm()
    return render(request, 'employee_register.html', {'form': form})




@require_http_methods(["GET", "POST"])
def employee_login_search(request):
    error_message = None

    if request.session.get('employee_id'):
        print(f"DEBUG: Session employee_id found: {request.session.get('employee_id')}. Redirecting to dashboard.")
        return redirect('employee_profile_dashboard')

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        print(f"DEBUG: POST request received for login. Employee ID entered: '{employee_id}', Password entered: '{password}'")

        if not employee_id or not password:
            error_message = "Please enter both Employee ID and password."
            messages.error(request, error_message)
            print(f"DEBUG: Validation failed: {error_message}")
            return render(request, 'employee_login_search.html', {'error_message': error_message})

        try:
            
            employee = Employee.objects.get(employee_id=employee_id, password=password) 
            if 'messages' in request.session:
                del request.session['messages']
            messages.get_messages(request)._loaded_data = [] 
            
            request.session['employee_id'] = employee.employee_id
            messages.success(request, f"Welcome, {employee.name}!")
            print("DEBUG: Employee found and session set (using insecure password check). Redirecting.")
            return redirect('employee_profile_dashboard')

        except Employee.DoesNotExist:
            error_message = "Invalid Employee ID or password."
            print(f"DEBUG: Employee with ID '{employee_id}' or matching password not found in database.")
        
        messages.error(request, error_message)
        return render(request, 'employee_login_search.html', {'error_message': error_message})

    else: 
        print("DEBUG: GET request received for login page.")
        return render(request, 'employee_login_search.html')



@require_http_methods(["GET"]) 
def employee_profile_dashboard(request):
    """
    Displays the logged-in employee's details and leave history.
    Requires an employee to be logged in (via session).
    """
    current_employee_id = request.session.get('employee_id')

    if not current_employee_id:
        messages.error(request, "Please log in to view your dashboard.")
        return redirect('employee_login_search')

    employee = None
    leave_history = []
    error_message = None

    try:
        employee = Employee.objects.get(employee_id=current_employee_id)
       
        leave_history = employee.leave_requests.all().order_by('-start_date')
    except Employee.DoesNotExist:
        
        if 'employee_id' in request.session:
            del request.session['employee_id']
        messages.error(request, "Your session is invalid. Please log in again.")
        return redirect('employee_login_search')

    context = {
        'employee': employee,
        'leave_history': leave_history,
    }
    return render(request, 'employee_profile_dashboard.html', context)



@require_http_methods(["GET", "POST"])
def submit_leave_request(request):
    """
    Handles displaying and processing the leave request form.
    Requires an employee to be logged in (via session).
    """
    current_employee_id = request.session.get('employee_id')

    if not current_employee_id:
        messages.error(request, "Please log in to submit a leave request.")
        return redirect('employee_login_search') 

    employee = None
    try:
        employee = Employee.objects.get(employee_id=current_employee_id)
    except Employee.DoesNotExist:
        if 'employee_id' in request.session:
            del request.session['employee_id']
        messages.error(request, "Your session is invalid. Please log in again.")
        return redirect('employee_login_search')

    if request.method == 'POST':
        leave_form = LeaveRequestForm(request.POST)
        if leave_form.is_valid():
            leave_request = leave_form.save(commit=False)
            leave_request.employee = employee 
            leave_request.status = 'Pending' 
            leave_request.save() 
            messages.success(request, "Your leave request has been submitted successfully!")
            return redirect('employee_profile_dashboard') 
        else:
            messages.error(request, "Please correct the errors in the leave request form.")
    else: 
        leave_form = LeaveRequestForm() 

    context = {
        'employee': employee, 
        'leave_form': leave_form,
    }
    return render(request, 'submit_leave_request.html', context)




def employee_logout(request):
    if 'employee_id' in request.session:
        del request.session['employee_id']
        messages.info(request, "You have been logged out.")
    return redirect('employee_login_search')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard') 
            else:
                messages.error(request, 'Invalid credentials or not an admin.')
        else:
            messages.error(request, 'Please enter both username and password.')

    return render(request, 'admin_login.html')







def is_admin(user):
    return user.is_staff

@login_required(login_url='/admin-login/')
@user_passes_test(is_admin)
def admin_dashboard(request):
    employees = Employee.objects.all()
    leaves = LeaveRequest.objects.all()
    return render(request, 'admin_dashboard.html', {
        'employees': employees,
        'leaves': leaves,
    })


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully.")
            return redirect('admin_employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})


def edit_employee(request, id):
    employee = get_object_or_404(Employee, emp_id= id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect('admin_employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'admin/edit_employee.html', {'form': form, 'employee': employee})


def delete_employee(request, id):
    employee = get_object_or_404(Employee, emp_id= id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
        return redirect('admin_employee_list')
    return render(request, 'admin/delete_employee.html', {'employee': employee})


def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'Approved'
    leave.employee.status = 'On Leave'
    leave.employee.save()
    leave.save()
    return redirect('admin_dashboard')


def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'Rejected'
    leave.save()
    return redirect('admin_dashboard')




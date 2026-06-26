from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Employee
from .forms import EmployeeForm
from rest_framework.generics import ListAPIView
from .serializers import EmployeeSerializer
from rest_framework.generics import RetrieveAPIView
from leaves.models import Leave
from payroll.models import Payroll
from attendance.models import Attendance


# Employee List
@login_required
def employee_list(request):

    employees = Employee.objects.select_related("user").all().order_by("employee_id")

    context = {
        "employees": employees
    }

    return render(
        request,
        "employees/employee_list.html",
        context
    )

# Add Employee
@login_required
def employee_create(request):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied("You are not authorized to add employees.")

    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('employee_list')

    else:
        form = EmployeeForm()

    return render(
        request,
        'employees/employee_form.html',
        {'form': form}
    )

# Update Employee
@login_required
def employee_update(request, pk):
    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    # Restrict editing of logged-in user's own employee details
    if employee.user == request.user:
        messages.error(request, "You cannot edit your own employee details from this list.")
        return redirect('employee_list')

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            instance=employee
        )

        if form.is_valid():
            form.save()
            return redirect('employee_list')

    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        'employees/employee_form.html',
        {'form': form}
    )

# Delete Employee
@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    # Restrict deleting of logged-in user themselves
    if employee.user == request.user:
        messages.error(request, "You cannot delete your own employee account.")
        return redirect('employee_list')

    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')

    return render(
        request,
        'employees/employee_confirm_delete.html',
        {'employee': employee}
    )

class EmployeeListAPI(ListAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetailAPI(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

@login_required
def employee_profile(request, pk):

    employee = get_object_or_404(Employee, pk=pk)

    attendance = Attendance.objects.filter(
        employee=employee
    ).order_by("-date")[:10]

    leaves = Leave.objects.filter(
        employee=employee
    ).order_by("-id")[:10]

    payroll = Payroll.objects.filter(
        employee=employee
    ).order_by("-id").last()

    context = {

        "employee": employee,

        "attendance": attendance,

        "leaves": leaves,

        "payroll": payroll,

        "attendance_count":
        Attendance.objects.filter(
            employee=employee
        ).count(),

        "leave_count":
        Leave.objects.filter(
            employee=employee
        ).count()

    }

    return render(

        request,

        "employees/employee_profile.html",

        context

    )

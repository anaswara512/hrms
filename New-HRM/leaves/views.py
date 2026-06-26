from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404

from employees.models import Employee
from .forms import LeaveForm
from leaves.models import Leave
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone


# Create your views here.
def leave_request(request):

    if request.method == 'POST':

        form = LeaveForm(request.POST)

        if form.is_valid():
            leave = form.save(commit=False)

            leave.employee = request.user.employee

            leave.save()

            return redirect('employee_dashboard')

    else:
        form = LeaveForm()

    return render(
        request,
        'leaves/request.html',
        {'form': form}
    )


@login_required
def leave_list(request):

    if request.user.role == 'EMPLOYEE':
        leaves = Leave.objects.filter(
            employee__user=request.user
        ).select_related("employee").order_by("-created_at")
        
        pending_count = leaves.filter(status="Pending").count()
        approved_count = leaves.filter(status="Approved").count()
        rejected_count = leaves.filter(status="Rejected").count()
    else:
        leaves = Leave.objects.select_related(
            "employee"
        ).all().order_by("-created_at")
        
        pending_count = Leave.objects.filter(status="Pending").count()
        approved_count = Leave.objects.filter(status="Approved").count()
        rejected_count = Leave.objects.filter(status="Rejected").count()

    context = {
        "leaves": leaves,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
    }

    return render(
        request,
        "leaves/leave_list.html",
        context
    )


@login_required
def apply_leave(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee_id = f"EMP{request.user.id:04d}"
        role = request.user.role
        if role == 'HR':
            designation = "HR Manager"
            default_dept = "Human Resource"
        elif role == 'ADMIN':
            designation = "System Admin"
            default_dept = "Administration"
        else:
            designation = "Trainee"
            default_dept = "General"

        employee = Employee.objects.create(
            user=request.user,
            employee_id=employee_id,
            phone="0000000000",
            department=default_dept,
            designation=designation,
            joining_date=timezone.now().date(),
            salary=0.00
        )

    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            leave.save()
            messages.success(request, "Leave request submitted successfully.")
            return redirect("leave_list")
    else:
        form = LeaveForm()

    return render(
        request,
        "leaves/apply_leave.html",
        {
            "form": form
        }
    )

@login_required
def approve_leave(request, pk):
    if request.user.role == 'EMPLOYEE':
        raise PermissionDenied("Employees are not authorized to approve leave requests.")

    leave = get_object_or_404(Leave, pk=pk)
    applicant_user = leave.employee.user

    if applicant_user == request.user:
        messages.error(request, "You cannot approve your own leave request.")
        return redirect("leave_list")

    if request.user.role == 'HR':
        if applicant_user and applicant_user.role in ['ADMIN', 'HR']:
            messages.error(request, "HR Managers cannot approve leave requests for Admin or other HR staff.")
            return redirect("leave_list")

    leave.status = "Approved"
    leave.save()
    messages.success(request, f"Leave request for {leave.employee} was successfully approved.")
    return redirect("leave_list")


@login_required
def reject_leave(request, pk):
    if request.user.role == 'EMPLOYEE':
        raise PermissionDenied("Employees are not authorized to reject leave requests.")

    leave = get_object_or_404(Leave, pk=pk)
    applicant_user = leave.employee.user

    if applicant_user == request.user:
        messages.error(request, "You cannot reject your own leave request.")
        return redirect("leave_list")

    if request.user.role == 'HR':
        if applicant_user and applicant_user.role in ['ADMIN', 'HR']:
            messages.error(request, "HR Managers cannot reject leave requests for Admin or other HR staff.")
            return redirect("leave_list")

    leave.status = "Rejected"
    leave.save()
    messages.success(request, f"Leave request for {leave.employee} was successfully rejected.")
    return redirect("leave_list")
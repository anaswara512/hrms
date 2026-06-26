from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from employees.models import Employee
from attendance.models import Attendance
from leaves.models import Leave
from accounts.decorators import hr_required
from payroll.models import Payroll


@login_required
def admin_dashboard(request):

    if request.user.role != "ADMIN":
        return redirect("/")

    context = {
        "total_employees": Employee.objects.count(),
        "total_attendance": Attendance.objects.count(),
        "pending_leaves": Leave.objects.filter(status="Pending").count(),
        "employees_list": Employee.objects.all().order_by("-id")[:5],
    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context,
    )


@login_required
@hr_required
def hr_dashboard(request):

    context = {
        "employees": Employee.objects.count(),
        "attendance": Attendance.objects.count(),
        "pending_leaves": Leave.objects.filter(
            status="Pending"
        ).count(),
    }

    return render(
        request,
        "dashboard/hr_dashboard.html",
        context
    )


from django.utils import timezone

@login_required
def employee_dashboard(request):

    try:
        employee = Employee.objects.get(user=request.user)

    except Employee.DoesNotExist:
        return render(
            request,
            "dashboard/employee_dashboard.html",
            {
                "error": "Employee profile not found."
            }
        )

    attendance = Attendance.objects.filter(employee=employee).order_by("-date")
    leaves = Leave.objects.filter(employee=employee).order_by("-created_at")
    
    today = timezone.now().date()
    today_attendance = Attendance.objects.filter(employee=employee, date=today).first()

    payroll = Payroll.objects.filter(
        employee=employee
    ).order_by("-id").first() # changed to order_by('-id') to match models/primary keys

    context = {

        "employee": employee,

        "attendance": attendance[:5],

        "leaves": leaves[:5],

        "payroll": payroll,

        "attendance_count": attendance.count(),

        "leave_count": leaves.count(),
        
        "today_attendance": today_attendance,

    }

    return render(
        request,
        "dashboard/employee_dashboard.html",
        context
    )
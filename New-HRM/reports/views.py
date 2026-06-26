from django.shortcuts import render
from employees.models import Employee
from attendance.models import Attendance
from leaves.models import Leave
from payroll.models import Payroll


def reports_dashboard(request):

    context = {

        "employees": Employee.objects.count(),

        "attendance": Attendance.objects.count(),

        "leaves": Leave.objects.count(),

        "payroll": Payroll.objects.count(),

    }

    return render(
        request,
        "reports/dashboard.html",
        context,
    )
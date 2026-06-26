from datetime import datetime, time
from django.utils import timezone
from django.shortcuts import redirect, render
from .models import Attendance
from django.db.models import Count
from django.http import JsonResponse
from employees.models import Employee

def check_in(request, employee_id):
    if request.method == "POST":
        try:
            employee = Employee.objects.get(id=employee_id)
            today = timezone.now().date()
            
            existing = Attendance.objects.filter(employee=employee, date=today).first()
            if existing:
                return JsonResponse({
                    "status": "error",
                    "message": "You have already checked in today!"
                })
            
            now_time = timezone.now().time()
            status = "Present"
            if now_time > time(9, 30):
                status = "Late"
                
            Attendance.objects.create(
                employee=employee,
                date=today,
                check_in=now_time,
                status=status
            )
            return JsonResponse({
                "status": "success",
                "message": f"Checked in successfully! Status: {status}"
            })
        except Employee.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Employee profile not found."
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })

    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    })


def check_out(request, attendance_id):
    if request.method == "POST":
        try:
            attendance = Attendance.objects.get(id=attendance_id)
            if attendance.check_out:
                return JsonResponse({
                    "status": "error",
                    "message": "Already checked out today."
                })
                
            now_time = timezone.now().time()
            attendance.check_out = now_time
            
            if attendance.check_in:
                d1 = datetime.combine(attendance.date, attendance.check_in)
                d2 = datetime.combine(attendance.date, now_time)
                diff = d2 - d1
                hours = diff.total_seconds() / 3600.0
                attendance.working_hours = round(hours, 2)
                
            attendance.save()
            return JsonResponse({
                "status": "success",
                "message": f"Checked out successfully! Worked: {attendance.working_hours} hours."
            })
        except Attendance.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Attendance record not found."
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
            
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    })


def monthly_report(request):

    report = (
        Attendance.objects
        .values('employee')
        .annotate(total=Count('id'))
    )

    return render(
        request,
        'attendance/report.html',
        {'report': report}
    )

def attendance_dashboard(request):

    attendance = Attendance.objects.select_related(
        "employee"
    ).order_by("-date")

    context = {

        "attendance": attendance,

        "present":

        Attendance.objects.filter(
            status="Present"
        ).count(),

        "late":

        Attendance.objects.filter(
            status="Late"
        ).count(),

        "absent":

        Attendance.objects.filter(
            status="Absent"
        ).count(),

    }

    return render(

        request,

        "attendance/dashboard.html",

        context

    )
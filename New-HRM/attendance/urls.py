from django.urls import path
from .views import attendance_dashboard, monthly_report
from .views import check_in, check_out


urlpatterns = [
    path(
        'report/',
        monthly_report,
        name='attendance_report'
    ),

    path(
        "checkin/<int:employee_id>/",
        check_in,
        name="check_in"
    ),

    path(
        "checkout/<int:attendance_id>/",
        check_out,
        name="check_out"
    ),

    path(
        "",
        attendance_dashboard,
        name="attendance_dashboard"
    ),
]
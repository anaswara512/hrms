from django.urls import path
from .views import (
    admin_dashboard,
    hr_dashboard,
    employee_dashboard,
)

urlpatterns = [
    path(
        "admin/",
        admin_dashboard,
        name="admin_dashboard",
    ),

    path(
        "",
        hr_dashboard,
        name="hr_dashboard",
    ),

    path(
        "employee/",
        employee_dashboard,
        name="employee_dashboard",
    ),
]
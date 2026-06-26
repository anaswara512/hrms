from django.urls import path
from .views import *

urlpatterns = [

    path(
        "",
        payroll_list,
        name="payroll_list"
    ),

    path(
        "generate/",
        generate_all_payroll,
        name="generate_all_payroll"
    ),

    path(
        "payslip/<int:id>/",
        generate_payslip,
        name="generate_payslip"
    ),

]

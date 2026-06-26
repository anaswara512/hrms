from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Payroll
from django.shortcuts import redirect

from employees.models import Employee

from .utils import generate_payroll


def generate_payslip(request, id):

    payroll = Payroll.objects.get(id=id)

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename="payslip.pdf"'
    )

    p = canvas.Canvas(response)

    p.drawString(
        100,
        800,
        f"Employee: {payroll.employee}"
    )

    p.drawString(
        100,
        780,
        f"Salary: {payroll.net_salary}"
    )

    p.save()

    return response

from django.shortcuts import render
from .models import Payroll


def payroll_list(request):

    payrolls = Payroll.objects.select_related(
        "employee"
    ).all()

    return render(

        request,

        "payroll/payroll_list.html",

        {

            "payrolls": payrolls

        }

    )

def generate_all_payroll(request):

    employees = Employee.objects.all()

    for emp in employees:

        generate_payroll(emp)

    return redirect("payroll_list")
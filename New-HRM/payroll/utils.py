from decimal import Decimal
from attendance.models import Attendance
from leaves.models import Leave
from .models import Payroll


def generate_payroll(employee):

    attendance = Attendance.objects.filter(
        employee=employee
    ).count()

    leave = Leave.objects.filter(
        employee=employee,
        status="Approved"
    ).count()

    salary = employee.salary

    salary_per_day = salary / 30

    deduction = Decimal(str(leave)) * salary_per_day

    bonus = Decimal(str(attendance * 50))

    tax = salary * Decimal('0.05')

    payroll = Payroll.objects.create(

        employee=employee,

        basic_salary=salary,

        deduction=deduction,

        bonus=bonus,

        tax=tax

    )

    return payroll
from django.db import models
from employees.models import Employee


class Payroll(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    month = models.CharField(
        max_length=20,
        default="June 2026"
    )

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    bonus = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    generated_on = models.DateField(
        auto_now_add=True
    )

    @property
    def net_salary(self):

        return (

            self.basic_salary

            + self.bonus

            - self.deduction

            - self.tax

        )

    def __str__(self):

        return self.employee.employee_id
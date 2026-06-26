from django.db import models
from employees.models import Employee

class Attendance(models.Model):

    STATUS_CHOICES = (

        ("Present", "Present"),

        ("Absent", "Absent"),

        ("Late", "Late"),

    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    working_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Present"
    )

    class Meta:

        unique_together = ("employee", "date")

    def __str__(self):

        return f"{self.employee} - {self.date}"
from django.db import models
from employees.models import Employee


class Leave(models.Model):

    LEAVE_TYPES = (

        ("Casual", "Casual"),
        ("Sick", "Sick"),
        ("Annual", "Annual"),

    )

    STATUS = (

        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),

    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.employee} - {self.leave_type}"
        )
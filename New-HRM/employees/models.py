from django.db import models
from accounts.models import User

class Employee(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    employee_id = models.CharField(max_length=20,unique=True)
    phone = models.CharField(max_length=15)

    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    joining_date = models.DateField()

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        if self.user:
            return self.user.username
        return self.employee_id
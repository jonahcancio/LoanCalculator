from django.db import models
from datetime import date
from django.utils import timezone

# Create your models here.
class Calculation(models.Model):
    loan_type = models.CharField(max_length=2)

    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_amortization = models.DecimalField(max_digits=12, decimal_places=2)
    total_interest = models.DecimalField(max_digits=12, decimal_places=2)
    loan_term = models.IntegerField()
    sum_payments = models.DecimalField(max_digits=12, decimal_places=2)

    loan_start_date = models.DateField(default=date.today())
    first_payment_date = models.DateField()
    loan_maturity_date = models.DateField()

    inquirer = models.ForeignKey("Inquirer", on_delete=models.SET_NULL, null=True, blank=True)


class Inquirer(models.Model):
    full_name = models.CharField(primary_key=True, max_length=80)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
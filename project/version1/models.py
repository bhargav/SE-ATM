from django.db import models

# Create your models here.
class Machine(models.Model):
	machine_id = models.IntegerField("MACHINE ID")
	location = models.CharField(max_length=200)
	minimum_atm_balance = models.DecimalField(decimal_places=2,max_digits=10)
	current_balance = models.DecimalField(decimal_places=2,max_digits=10)
	last_refill_date = models.DateTimeField('LAST REFILL DATE')
	next_maintainence_date = models.DateTimeField('NEXT MAINTAINENCE DATE')
	
class Account_Ext(models.Model):
	acc_num = models.IntegerField("Account Number")
	atmcard_num = models.IntegerField("ATM Card Number")
	name = models.CharField(max_length=100)
	phone_num = models.IntegerField("Phone NUMBER")

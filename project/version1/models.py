from django.db import models

# Create your models here.
class Machine(models.Model):
	machine_id = models.IntegerField("MACHINE ID",primary_key=True)
	location = models.CharField("LOCATION",max_length=200)
	minimum_atm_balance = models.DecimalField("MINIMUM ATM BALANCE",decimal_places=2,max_digits=10)
	current_balance = models.DecimalField("BALANCE",decimal_places=2,max_digits=10)
	last_refill_date = models.DateTimeField('LAST REFILL DATE')
	next_maintainence_date = models.DateTimeField('NEXT MAINTAINENCE DATE')


class MachineRefill(models.Model):
	refill_id = models.IntegerField("REFILL ID",primary_key=True)
	machine_id = models.ForeignKey(Machine)
	refill_date = models.DateTimeField('REFILL DATE')
	previous_balance = models. DecimalField("PREVIOUS ATM BALANCE",decimal_places=2,max_digits=10)
	amount_refilled = models.DecimalField("AMOUNT REFILLED",decimal_places=2,max_digits=10)
	

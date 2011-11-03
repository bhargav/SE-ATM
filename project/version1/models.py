from django.db import models

# Create your models here.
class Machine(models.Model):
	machine_id = models.IntegerField()
	location = models.CharField(max_length=200)
	minimum_atm_balance = models.IntegerField()
	current_balance = models.IntegerField()
	last_refill_date = models.DateTimeField('LAST REFILL DATE')
	next_maintainence_date = models.DateTimeField('NEXT MAINTAINENCE DATE')

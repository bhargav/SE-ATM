from django.db import models
# Create your models here.
class Machine(models.Model):
	machine_id = models.IntegerField("MACHINE ID",primary_key=True)
	location = models.CharField("LOCATION",max_length=200)
	minimum_atm_balance = models.DecimalField("MINIMUM ATM BALANCE",decimal_places=2,max_digits=10)
	current_balance = models.DecimalField("BALANCE",decimal_places=2,max_digits=10)
	last_refill_date = models.DateTimeField('LAST REFILL DATE')
	next_maintainence_date = models.DateTimeField('NEXT MAINTAINENCE DATE')
	def __unicode__(self):
		return str(self.machine_id)


class MachineRefill(models.Model):
	refill_id = models.IntegerField("REFILL ID",primary_key=True)
	machine_id = models.ForeignKey(Machine)
	refill_date = models.DateTimeField('REFILL DATE')
	previous_balance = models. DecimalField("PREVIOUS ATM BALANCE",decimal_places=2,max_digits=10)
	amount_refilled = models.DecimalField("AMOUNT REFILLED",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.refill_id)
	
class Account_Ext(models.Model):
	acc_num = models.BigIntegerField("Account Number",primary_key=True)
	atmcard_num = models.BigIntegerField("ATM Card Number")
	name = models.CharField("NAME",max_length=100)
	phone_num = models.BigIntegerField("Phone NUMBER")
	balance = models.DecimalField("Balance",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.acc_num)
	
class ATM_Card(models.Model):
	atmcard_num = models.ForeignKey(Account_Ext)
	name = models.CharField("NAME ON CARD",max_length=100)
	pin = models.IntegerField("PIN", max_length=4)
	date_of_issue = models.DateTimeField('DATE OF ISSUE')
	expiry_date = models.DateTimeField('EXPIRY DATE')
	address = models.CharField("ADDRESS",max_length=300)
	two_factor = models.BooleanField("TWO FACTOR AUTHENTICATION STATUS")
	phone_num = models.BigIntegerField("PHONE NUMBER FOR AUTHENTICATION")
	card_status = models.BooleanField("CARD STATUS")
	def __unicode__(self):
		return str(self.atmcard_num)
	
class Transaction(models.Model):
	atmcard_num = models.ForeignKey(Account_Ext)
	machine_id = models.ForeignKey(Machine)
	tid = models.IntegerField("TRANSACTION ID",primary_key=True)
	date_time = models.DateTimeField("DATE TIME OF TRANSACTION")
	status = models.CharField("STATUS",max_length = 100)
	rescode = models.IntegerField("RESPONSE CODE")
	type_trans = models.CharField("TRANSACTION TYPE",max_length = 100)
	class Meta:
		abstract = True

class Balance_Enquiry(Transaction):
	bal_amount = models.DecimalField("BALANCE AMOUNT",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.tid)
		
class Phone_change(Transaction):
	prev_phone = models.BigIntegerField("PREVIOUS PHONE NO")
	new_phone = models.BigIntegerField("NEW PHONE NO")
	def __unicode__(self):
		return str(self.tid)
		
class Pin_change(Transaction):
	prev_pin = models.IntegerField("PREVIOUS PIN")
	new_pin = models.IntegerField("NEW PIN")
	def __unicode__(self):
		return str(self.tid)		
	
class Cash_Transfer(Transaction):
	ben_acc_num = models.BigIntegerField("BENEFICIARY ACCOUNT NUMBER")
	ben_name = models.CharField("BENEFICIARY NAME",max_length = 100)
	amt_trans = models.DecimalField("AMOUNT",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.tid)	
	
class Cash_Withdrawl(Transaction):
	amt_with = models.DecimalField("AMOUNT WITHDRAWN",decimal_places=2,max_digits=10)
	cur_bal = models.DecimalField("CURRENT BALANCE",decimal_places=2,max_digits=10)
	#denomination 
	def __unicode__(self):
		return str(self.tid)	

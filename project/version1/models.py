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
	acc_num = models.BigIntegerField("Account Number")
	atmcard_num = models.BigIntegerField("ATM Card Number")
	name = models.CharField("NAME",max_length=100)
	phone_num = models.BigIntegerField("Phone NUMBER")
	
class ATM_Card(models.Model):
	acc_ext = models.ForeignKey(Account_Ext)
	atm_cardnum = models.BigIntegerField("ATM CARD NUMBER")
	name = models.CharField("NAME ON CARD",max_length=100)
	acc_num = models.BigIntegerField("ACCOUNT NUMBER LINKED")
	pin = models.IntegerField("PIN")
	date_of_issue = models.DateTimeField('DATE OF ISSUE')
	expiry_date = models.DateTimeField('EXPIRY DATE')
	address = models.CharField("ADDRESS",max_length=300)
	two_factor = models.BooleanField("TWO FACTOR AUTHENTICATION STATUS")
	phone_num = models.BigIntegerField("PHONE NUMBER FOR AUTHENTICATION")
	card_status = models.BooleanField("CARD STATUS")
	
class Transaction(models.Model):
	atm_card = models.ForeignKey(ATM_Card)
	atm_machine = models.ForeignKey(Machine)
	tid = models.IntegerField("TRANSACTION ID")
	atm_cardnum = models.BigIntegerField("ATM CARD NUMBER")
	date_time = models.DateTimeField("DATE TIME OF TRANSACTION")
	status = models.CharField("STATUS",max_length = 100)
	rescode = models.IntegerField("RESPONSE CODE")
	type_trans = models.CharField("TRANSACTION TYPE",max_length = 100)
	atm_uid = models.IntegerField("ATM UID")
	atm_branch = models.CharField("ATM BRANCH",max_length = 100)
	
	class Meta:
		abstract = True

class Balance_Enquiry(Transaction):
	trans_num = models.BigIntegerField("TRANSACTION NUMBER")
	bal_amount = models.DecimalField("BALANCE AMOUNT",decimal_places=2,max_digits=10)
		
class Pin_change(Transaction):
	trans_num = models.IntegerField("TRANSACTION NUMBER")
	prev_pin = models.IntegerField("PREVIOUS PIN")
	new_pin = models.IntegerField("NEW PIN")
	success = models.BooleanField("STATUS")

class Cash_Transfer(Transaction):
	trans_num = models.IntegerField("TRANSACTION NUMBER")
	ben_acc_num = models.BigIntegerField("BENEFICIARY ACCOUNT NUMBER")
	ben_name = models.CharField("BENEFICIARY NAME",max_length = 100)
	amt_trans = models.DecimalField("AMOUNT",decimal_places=2,max_digits=10)
	success = models.BooleanField("STATUS")

class Cash_Withdrawl(Transaction):
	trans_num = models.IntegerField("TRANSACTION NUMBER")
	amt_with = models.DecimalField("AMOUNT WITHDRAWN",decimal_places=2,max_digits=10)
	cur_bal = models.DecimalField("CURRENT BALANCE",decimal_places=2,max_digits=10)
	success = models.BooleanField("STATUS")
	#denomination 


from django.db import models
from decimal import *
# Admin model stores the information of adiministrator. 
# It has 2 fields
# Admin_id -->char(100)
# password -->char(100)
class Admin(models.Model):
	Admin_id = models.CharField("ADMIN ID",max_length=100,primary_key=True)
	Password = models.CharField("PASSWORD",max_length=100)
	def __unicode__(self):
		return str(self.Admin_id)

# Machine model stores the information of ATM_Machine 
# It has 6 fields
# location ---> Char(200)
# minimum_atm_balance ---> Decimal
# current_balance ----> Decimal
# last_refill_date ----> DateTimeField
# next_maintainence_date ----> DateTimeField
class Machine(models.Model):
	machine_id = models.IntegerField("MACHINE ID",primary_key=True)
	location = models.CharField("LOCATION",max_length=200)
	minimum_atm_balance = models.DecimalField("MINIMUM ATM BALANCE",decimal_places=2,max_digits=10)
	current_balance = models.DecimalField("BALANCE",decimal_places=2,max_digits=10)
	last_refill_date = models.DateTimeField('LAST REFILL DATE')
	next_maintainence_date = models.DateTimeField('NEXT MAINTAINENCE DATE')
	def __unicode__(self):
		return str(self.machine_id)

# MachineRefill model stores the information of refill for ATM machine. 
# It has 5 fields
# refill_id -->Integer
# machine_id ---> ForeignKey of Machine
# refill_date ---> DateTimeField
# previous_balance ---> DecimalField
# amount_refilled ----> Decimal
class MachineRefill(models.Model):
	refill_id = models.IntegerField("REFILL ID",primary_key=True)
	machine_id = models.ForeignKey(Machine)
	refill_date = models.DateTimeField('REFILL DATE')
	previous_balance = models. DecimalField("PREVIOUS ATM BALANCE",decimal_places=2,max_digits=10)
	amount_refilled = models.DecimalField("AMOUNT REFILLED",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.refill_id)
	
# Account_Ext model stores the information of account with atm card information. 
# It has 5 fields
# acc_num = BigInteger
# atmcard_num ---> BigInteger
# name --> Char
# phone_num --> BigInteger
# balance --> Decimal
class Account_Ext(models.Model):
	acc_num = models.BigIntegerField("Account Number",primary_key=True)
	atmcard_num = models.BigIntegerField("ATM Card Number")
	name = models.CharField("NAME",max_length=100)
	phone_num = models.BigIntegerField("Phone NUMBER")
	balance = models.DecimalField("Balance",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.acc_num)
	
# ATM_Card model stores the information of ATM cars 
# It has 9 fields
# atmcard_num ---> ForeignKey of Account_Ext
# name ---> Char(100)
# pin ---> Integer
# date_of_issue ---> DateTimeField
# expiry_date ---> DateTimeField
# address --> Char(300)
# two_factor ---> Boolean
# phone_num ---> BigInteger
# card_status ---> Boolean
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

# Transaction() is the abstract class which has sub-classes  
# It has 7 fields
# atmcard_num ---> ForeignKey of Account_Ext
# machine_id ---> ForeignKey of Machine
# tid ---> Integer
# date_time ---> DateTimeField
# status ---> Char(100)
# rescode ---> Integer
# type_trans ---> Char(100)
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

# Balance_Enquiry() is the inherited class of trasaction class
# It has 1 fields
# bal_amount ----> Decimal
class Balance_Enquiry(Transaction):
	bal_amount = models.DecimalField("BALANCE AMOUNT",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.tid)
		
# pin_change() is the inherited class of trasaction class
# It has 2 fields
# prev_pin ---> Integer
# new_pin ---> Integer	
class Pin_change(Transaction):
	prev_pin = models.IntegerField("PREVIOUS PIN")
	new_pin = models.IntegerField("NEW PIN")
	def __unicode__(self):
		return str(self.tid)
	
# Cash_Transfer() is the inherited class of trasaction class
# It has 3 fields
# ben_acc_num ---> BigInteger
# ben_name ---> Char(100)
# amt_trans ----> Decimal
class Cash_Transfer(Transaction):
	ben_acc_num = models.BigIntegerField("BENEFICIARY ACCOUNT NUMBER")
	ben_name = models.CharField("BENEFICIARY NAME",max_length = 100)
	amt_trans = models.DecimalField("AMOUNT",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.tid)	
	
# Cash_Withdrawl() is the inherited class of trasaction class
# It has 2 fields
# amt_with ---> Decimal
# cur_bal ---> Decimal
class Cash_Withdrawl(Transaction):
	amt_with = models.DecimalField("AMOUNT WITHDRAWN",decimal_places=2,max_digits=10)
	cur_bal = models.DecimalField("CURRENT BALANCE",decimal_places=2,max_digits=10)
	#denomination 
	def __unicode__(self):
		return str(self.tid)	

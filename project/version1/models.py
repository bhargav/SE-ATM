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
	def save(self, *args, **kwargs):
		if(self.machine_id<=0):
			raise Exception, "MACHINE ID SHOULD BE NON ZERO POSITIVE"
		else:
			if(self.minimum_atm_balance<0):
				raise Exception, "MINIMUM ATM BALANCE SHOULD BE POSITIVE"
			else:
				if(self.current_balance<0):
					raise Exception, "BALANCE SHOULD BE POSITIVE"
				else:			
					super(Machine, self).save()
					
class MachineRefill(models.Model):
	refill_id = models.IntegerField("REFILL ID",primary_key=True)
	machine_id = models.ForeignKey(Machine)
	refill_date = models.DateTimeField('REFILL DATE')
	previous_balance = models. DecimalField("PREVIOUS ATM BALANCE",decimal_places=2,max_digits=10)
	amount_refilled = models.DecimalField("AMOUNT REFILLED",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.refill_id)
	def save(self, *args, **kwargs):
		if(self.refill_id<=0):
			raise Exception, "REFILL ID SHOULD BE NON ZERO POSITIVE"
		else:
			if(self.previous_balance<0):
				raise Exception, "PREVIOUS ATM BALANCE SHOULD BE POSITIVE"
			else:
				if(self.amount_refilled<0):
					raise Exception, "AMOUNT REFILLED SHOULD BE POSITIVE"
				else:			
					super(MachineRefill, self).save()	
	
class Account_Ext(models.Model):
	acc_num = models.BigIntegerField("Account Number",primary_key=True)
	name = models.CharField("NAME",max_length=100)
	phone_num = models.BigIntegerField("Phone NUMBER")
	balance = models.DecimalField("Balance",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.acc_num)
	def save(self, *args, **kwargs):
		if(self.acc_num > 0):
			if(len(str(self.acc_num)) == 12):
				if(self.phone_num<=0):
					raise Exception, "PHONE NUMBER SHOULD BE NON ZERO POSITIVE"
				else:	
					if(len(str(self.phone_num)) != 10):
						raise Exception, "PHONE NUMBER LENGTH SHOULD BE 10"
					else:
						if(self.balance<0):
							raise Exception, "BALANCE SHOULD BE POSITIVE"
						else:		
							super(Account_Ext, self).save()
			else:
				raise Exception, "ACCOUNT NUMBER LENGTH SHOULD BE 12"	
		else:
			raise Exception, "ACCOUNT NUMBER SHOULD BE NON ZERO POSITIVE"
	
class ATM_Card(models.Model):
	atmcard_num = models.BigIntegerField("ATM Card Number")
	account_num = models.ForeignKey(Account_Ext)
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
	def save(self, *args, **kwargs):
		if(self.atmcard_num > 0):
			if(len(str(self.atmcard_num)) == 4):
				if(self.pin <= 0):
					raise Exception, "PIN NUMBER SHOULD BE NON ZERO POSITIVE"
				else:	
					if(len(str(self.pin)) != 4):
						raise Exception, "PIN NUMBER LENGTH SHOULD BE 4"
					else:
						if(self.expiry_date<=self.date_of_issue):
							raise Exception, "EXPIRY DATE SHOULD BE AFTER THE ISSUE DATE"
						else:
							if(self.phone_num<=0):
								raise Exception, "PHONE NUMBER SHOULD BE NON ZERO POSITIVE"
							else:
								if(len(str(self.phone_num))!=10):
									raise Exception, "PHONE NUMBER LENGTH SHOULD BE 10"
								else:				
									super(ATM_Card, self).save()
			else:
				raise Exception, "ATM CARD NUMBER LENGTH SHOULD BE 4"	
		else:
			raise Exception, "ATM CARD NO. SHOULD BE NON ZERO POSITIVE"	
	
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
	def save(self, *args, **kwargs):
		if(self.tid<=0):
			raise Exception, "TRANSACTION ID SHOULD BE NON ZERO POSITIVE"
		else:
			if(self.rescode<0):
				raise Exception, "RESPONSE CODE SHOULD BE POSITIVE"
			else:
				if(self.bal_amount<0):
					raise Exception, "BALANCE AMOUNT SHOULD BE POSITIVE"
				else:			
					super(Balance_Enquiry, self).save()	
		
class Phone_change(Transaction):
	prev_phone = models.BigIntegerField("PREVIOUS PHONE NO")
	new_phone = models.BigIntegerField("NEW PHONE NO")
	def __unicode__(self):
		return str(self.tid)
	def save(self, *args, **kwargs):
		if(self.tid<=0):
			raise Exception, "TRANSACTION ID SHOULD BE NON ZERO POSITIVE"
		else:
			if(self.rescode<0):
				raise Exception, "RESPONSE CODE SHOULD BE POSITIVE"
			else:
				if(self.prev_phone<=0):
					raise Exception, "PREVIOUS PHONE NO SHOULD BE POSITIVE"
				else:
					if(len(str(self.prev_phone))!=10):
						raise Exception, "PREV PHONE NO SHOULD BE OF LENGTH 10"
					else:	
						if(self.new_phone<=0):
							raise Exception, "NEW PHONE NO SHOULD BE POSITIVE"
						else:
							if(len(str(self.new_phone))!=10):
								raise Exception, "NEW PHONE NO SHOULD BE OF LENGTH 10"
							else:			
								super(Phone_change, self).save()		

class Pin_change(Transaction):
	prev_pin = models.IntegerField("PREVIOUS PIN")
	new_pin = models.IntegerField("NEW PIN")
	def __unicode__(self):
		return str(self.tid)
	def save(self, *args, **kwargs):
		if(self.tid<=0):
			raise Exception, "TRANSACTION ID SHOULD BE NON ZERO POSITIVE"
		else:
			if(self.rescode<0):
				raise Exception, "RESPONSE CODE SHOULD BE POSITIVE"
			else:
				if(self.prev_pin<=0):
					raise Exception, "PREVIOUS PIN NO SHOULD BE POSITIVE"
				else:
					if(len(str(self.prev_pin))!=4):
						raise Exception, "PREVIOUS PIN NO SHOULD BE OF LENGTH 4"
					else:	
						if(self.new_pin<=0):
							raise Exception, "NEW PIN NO SHOULD BE POSITIVE"
						else:
							if(len(str(self.new_pin))!=4):
								raise Exception, "NEW PIN NO SHOULD BE OF LENGTH 4"
							else:			
								super(Pin_change, self).save()					
	
class Cash_Transfer(Transaction):
	ben_acc_num = models.BigIntegerField("BENEFICIARY ACCOUNT NUMBER")
	ben_name = models.CharField("BENEFICIARY NAME",max_length = 100)
	amt_trans = models.DecimalField("AMOUNT",decimal_places=2,max_digits=10)
	def __unicode__(self):
		return str(self.tid)
	def save(self, *args, **kwargs):
		if(self.tid<=0):
			raise Exception, "TRANSACTION ID SHOULD BE NON ZERO POSITIVE"
		else:
			if(self.rescode<0):
				raise Exception, "RESPONSE CODE SHOULD BE POSITIVE"
			else:
				if(self.ben_acc_num<0):
					raise Exception, "BENEFICIARY ACCOUNT NUMBER SHOULD BE NON ZERO POSITIVE"
				else:
					if(len(str(self.ben_acc_num))!=12):
						raise Exception, "BENEFICIARY ACCOUNT NUMBER SHOULD BE OF LENGTH 12"
					else:
						if(self.amt_trans<=0):
							raise Exception, "AMOUNT SHOULD BE NON ZERO POSITIVE"
						else:	
							super(Cash_Transfer, self).save()			
	
class Cash_Withdrawl(Transaction):
	amt_with = models.DecimalField("AMOUNT WITHDRAWN",decimal_places=2,max_digits=10)
	cur_bal = models.DecimalField("CURRENT BALANCE",decimal_places=2,max_digits=10)
	#denomination 
	def __unicode__(self):
		return str(self.tid)
	def save(self, *args, **kwargs):
		if(self.tid<=0):
			raise Exception, "TRANSACTION ID SHOULD BE NON ZERO POSITIVE"
		else:
			if(self.rescode<0):
				raise Exception, "RESPONSE CODE SHOULD BE POSITIVE"
			else:
				if(self.amt_with<=0):
					raise Exception, "AMOUNT WITHDRAWN SHOULD BE POSITIVE"
				else:
					if(self.cur_bal<0):
						raise Exception, "CURRENT BALANCE SHOULD BE ZERO OR POSITIVE"
					else:
						if(self.amt_with>self.cur_bal):
							raise Exception, "WITHDRAWAL AMOUNT IS MORE THAN CURRENT BALANCE"
						else:	
							super(Cash_Withdrawl, self).save()		

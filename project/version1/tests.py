from django.test import TestCase, Client
from version1.models import *
import datetime

class MachineTestCase(TestCase):
	def setUp(self):
		self.data_1 = Machine(1,"Delhi", 100.00, 500.00, datetime.datetime.now(), datetime.datetime.now())
		self.data_1.save()

	def testMachine(self):
		self.assertEqual(Machine.objects.all().count(), 1)
		tdata = Machine.objects.get(machine_id = 1)
		self.assertEqual(tdata.location, "Delhi")
		self.assertEqual(tdata.current_balance, 500.00)
		self.assertEqual(tdata.minimum_atm_balance, 100.00)
		self.assertLess(tdata.last_refill_date, datetime.datetime.now())
	
	def testMachine_negative_money(self):
		temp = self.data_1.current_balance
		self.data_1.current_balance = -100
		self.assertRaises(Exception, self.data_1.save)
		self.data_1 = Machine.objects.get(machine_id = 1)
		self.data_1.minimum_atm_balance = -1
		self.assertRaises(Exception, self.data_1.save)
		self.data_1.minimum_atm_balance = temp
	
	def testMachine_negative_id(self):
		self.data_1 = Machine.objects.get(machine_id = 1)
		self.data_1.machine_id = -12
		self.assertRaises(Exception, self.data_1.save)

	def testMachine_checkUpdate(self):
		data = Machine.objects.get(machine_id = 1)
		data.current_balance = 1000.00
		data.save()
		self.assertEqual(Machine.objects.all().count(), 1)

		data_temporary = Machine.objects.get(machine_id = 1)
		self.assertEqual(data_temporary.current_balance, 1000.00)
		data_temporary.minimum_atm_balance = 100.50
		data_temporary.save()
		self.assertEqual(Machine.objects.all().count(), 1)		

		data = Machine.objects.get(machine_id = 1)
		self.assertEqual(data.minimum_atm_balance, 100.50)

class AccountExtensionTestCase(TestCase):
	def setUp(self):
		self.data = Account_Ext(123456789012, "M", 9646818259, 100.00)
		self.data.save()
	
	def testAccountExt(self):
		self.assertEqual(Account_Ext.objects.all().count(), 1)
		t = Account_Ext.objects.all()[0]
		self.assertEqual(t.acc_num, 123456789012)
		self.assertEqual(t.name, "M")
		self.assertEqual(t.phone_num, 9646818259)
		self.assertEqual(t.balance, 100.00)

	def testAccountExt_negative_fields(self):
		t = Account_Ext.objects.all()[0]
		t.acc_num = 123
		self.assertRaises(Exception, t.save)

		t = Account_Ext.objects.all()[0]
		t.acc_num = -10
		self.assertRaises(Exception, t.save)

		t = Account_Ext.objects.all()[0]
		t.phone_num = -1245465
		self.assertRaises(Exception, t.save)

		t = Account_Ext.objects.all()[0]
		t.phone_num = 1234
		self.assertRaises(Exception, t.save)

		t = Account_Ext.objects.all()[0]
		t.balance = - 10
		self.assertRaises(Exception, t.save)
	
	def testAccountExt_checkUpdate(self):
		t = Account_Ext.objects.all()[0]
		t.balance = 12345.00
		t.save()
		self.assertEqual(Account_Ext.objects.all().count(), 1)
		temp = Account_Ext.objects.all()[0]
		
class ATMCardTestCase(TestCase):
	def setUp(self):
		t = Account_Ext(123456789012, "M", 9646818259, 100.00)
		t.save()
		self.data = ATM_Card(account_num=Account_Ext.objects.get(acc_num=123456789012), atmcard_num = 2311, name="M", pin=1234, date_of_issue=datetime.datetime.now(), expiry_date=datetime.datetime(2012, 11, 10, 12, 00), address="12 B, New Delhi", two_factor=False, phone_num=9646818259, card_status=True)		
		self.data.save()

	def testATMCard(self):
		self.assertEqual(ATM_Card.objects.all().count(), 1)
		card = ATM_Card.objects.all()[0]
		self.assertEqual(card.account_num_id,123456789012)
		self.assertEqual(card.atmcard_num, 2311)
		self.assertEqual(card.phone_num, 9646818259)
		self.assertEqual(card.card_status, True)
	
	def testATMCard_checkPrimaryKey(self):
		t = ATM_Card.objects.all()[0]
		t.account_num_id = 2
		self.assertRaises(Exception, t.save)
	
	def testATMCard_checkUpdate(self):
		t = ATM_Card.objects.all()[0]
		t.pin=1212
		t.save()

		self.assertEqual(ATM_Card.objects.all().count(), 1)
		self.assertEqual(ATM_Card.objects.all()[0].pin, 1212)
	
	def testATMCard_invalidFields(self)
		t = ATM_Card.objects.all()[0]
		



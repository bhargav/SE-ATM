# Create your views here.
from version1.models import Account_Ext
from version1.models import ATM_Card
from version1.models import Balance_Enquiry
from version1.models import Transaction
from version1.models import Cash_Withdrawl
from version1.models import Cash_Transfer
from decimal import *
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404 
import datetime

def index(request):
    Account_holder_list = Account_Ext.objects.all()
    return render_to_response('version1/index.html', locals())

def validatecard(request):
	global session
	p = get_object_or_404(Account_Ext, pk=request.GET['cardnumber'])
	session = request.GET['cardnumber']
	return render_to_response('version1/pincode.html', locals())
    
def validatepin(request):
    #Account_holder_list = Account_Ext.objects.all()
    global session
    pin = ATM_Card.objects.filter(pin=request.GET['pincode'],atmcard_num=session)
    if pin:
		return render_to_response('version1/options.html', locals())	
    return HttpResponse("Your pincode is not valid")

def balanceenquiry(request):
	global session
	[t_acc] = Account_Ext.objects.filter(atmcard_num=session)
	#mach = Machine.objects.filter(machine_id =1)
	t = Balance_Enquiry(atmcard_num_id = session, machine_id_id = 1,tid = 1,date_time = datetime.datetime.now(),status = "Completed",rescode = 1,type_trans = "Balance Enquiry",bal_amount=t_acc.balance)
	t.save()
	bal = t_acc.balance
	return render_to_response('version1/balance.html', locals())
	
def cashwithdrawal(request):
	return render_to_response('version1/cashwithdrawal.html', locals())
	
def mcashwithdrawal(request):
	global session
	t_acc = Account_Ext.objects.get(atmcard_num=session)
	amount = request.GET['cw_amount']	
	t_acc.balance = t_acc.balance - Decimal(amount)
	t_acc.save()
	ta = Cash_Withdrawl(atmcard_num_id = session, machine_id_id =1, date_time = datetime.datetime.now(),status = "Completed",rescode = 2,type_trans = "Cash Withdrawal",amt_with = Decimal(amount),cur_bal = t_acc.balance)
	ta.save()
	return render_to_response('version1/mcashwithdrawal.html', locals())
	
def cashtransfer(request):
	return render_to_response('version1/cashtransfer.html', locals())

def mcashtransfer(request):
	global session
	amount = request.GET['ct_transfer']
	accnum = request.GET['ACC_Num']
	t_acc1 = Account_Ext.objects.get(atmcard_num=session)
	t_acc2 = Account_Ext.objects.get(atmcard_num=int(accnum))
	t_acc1.balance = t_acc1.balance - Decimal(amount)
	t_acc2.balance = t_acc2.balance + Decimal(amount)
	ta = Cash_Transfer(atmcard_num_id = session, machine_id_id =1, date_time = datetime.datetime.now(),status = "Completed",rescode = 3,type_trans = "Cash Withdrawal",ben_acc_num = int(accnum),ben_name = t_acc2.name,amt_trans = Decimal(amount))
	ta.save()
	t_acc1.save()
	t_acc2.save()
	return render_to_response('version1/mcashtransfer.html', locals())

def pinchange(request):
	return render_to_response('version1/pinchange.html', locals())
	
def fastcash(request):
	return render_to_response('version1/fastcash.html', locals())
	
def mfastcash(request):
	global session
	t_acc = Account_Ext.objects.get(atmcard_num=session)
	amount = request.GET['Fcash']	
	t_acc.balance = t_acc.balance - Decimal(amount)
	t_acc.save()
	ta = Cash_Withdrawl(atmcard_num_id = session, machine_id_id =1, date_time = datetime.datetime.now(),status = "Completed",rescode = 2,type_trans = "Cash Withdrawal",amt_with = Decimal(amount),cur_bal = t_acc.balance)
	ta.save()
	return render_to_response('version1/mcashwithdrawal.html', locals())

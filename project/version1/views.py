# Create your views here.
from version1.models import Account_Ext
from version1.models import ATM_Card
from version1.models import Balance_Enquiry
from version1.models import Transaction
from version1.models import Cash_Withdrawl
from version1.models import Cash_Transfer
from decimal import *
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect 
import datetime
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):
	if 'cardnumber' in request.session:
		return redirect('/user/validatepin/')
		
	if request.method == 'POST':
		cardnum = request.POST['cardnumber']
		card = ATM_Card.objects.filter(atmcard_num=cardnum)
		if not card:
			# There is no ATM card with that card number
			return HttpResponse("Invalid Card")
		elif not card[0].card_status:
			return HttpResponse("Blocked")
		else:
			date = datetime.datetime.now()
			if(card[0].expiry_date < date):
				return HttpResponse("Expired")
			else:
				request.session['cardnumber'] = cardnum
				return redirect('/user/validatepin/')
	return render_to_response('finale/index.html')

@csrf_protect
def validatepin(request):
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' in request.session:
		return redirect('/user/options/')
		
	atmcard = ATM_Card.objects.get(atmcard_num=request.session['cardnumber'])
	username = atmcard.name
	request.session['username'] = username
	
	if request.method == 'POST':
		cardpin = request.POST['pincode']
		print cardpin, atmcard.pin
		if int(atmcard.pin) == int(cardpin):
			request.session['pinverified'] = True
			return redirect('/user/options')
		# Update the number of attempts accordingly
		if 'pinattempt' not in request.session:
			request.session['pinattempt'] = 1
		else:
			request.session['pinattempt'] = request.session['pinattempt'] + 1
		
		if request.session['pinattempt'] == 1:
		# Message to be displayed
				pinmessage = 1
		elif request.session['pinattempt'] == 2:
				pinmessage = 2
		else:
				pinmessage = 3
				atmcard.card_status = False
				atmcard.save()
				request.session.flush()
	return render_to_response('finale/pincode.html', locals())

@csrf_protect
def options(request):
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')
		
	username = request.session['username']
	return render_to_response('finale/options.html', locals())

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
	
def changepin(request):
	global session
	[atmcard]=ATM_Card.objects.filter(atmcard_num=session)
	if(str(atmcard.pin)==request.GET['pincode'] and request.GET['newpincode']==request.GET['confirmpincode'] and request.GET['pincode']!=request.GET['confirmpincode'] and int(request.GET['confirmpincode'])>999):	
		atmcard.pin=request.GET['newpincode']
		atmcard.save()
		return HttpResponse("Your pincode is changed")
	else:	
		return HttpResponse("Your pincode is not changed")
	
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

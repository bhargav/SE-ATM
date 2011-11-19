# Create your views here.
from version1.models import Account_Ext
from version1.models import ATM_Card
from version1.models import Balance_Enquiry
from version1.models import Transaction
from version1.models import Cash_Withdrawl
from version1.models import Cash_Transfer
from version1.models import *
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

@csrf_protect
def balanceenquiry(request):
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')	
	atmcard = ATM_Card.objects.get(atmcard_num=request.session['cardnumber'])
	t_acc = Account_Ext.objects.get(acc_num=str(atmcard.account_num))
	t = Balance_Enquiry(atmcard_num_id = request.session['cardnumber'], machine_id_id = 1,tid = 1,date_time = datetime.datetime.now(),status = "Completed",rescode = 1,type_trans = "Balance Enquiry",bal_amount=t_acc.balance)
	t.save()
	bal = t_acc.balance
	username=atmcard.name
	return render_to_response('finale/balance.html', locals())

@csrf_protect	
def cashwithdrawal(request):
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')
	username=request.session['username']
	if request.method == 'POST':
		atmcard = ATM_Card.objects.get(atmcard_num=request.session['cardnumber'])
		t_acc = Account_Ext.objects.get(acc_num=str(atmcard.account_num))
		if(Decimal(t_acc.balance)>Decimal(request.POST['amount'])):
			t_acc.balance = t_acc.balance - Decimal(request.POST['amount'])
			t_acc.save()
			t = Cash_Withdrawl(atmcard_num_id = request.session['cardnumber'], machine_id_id = 1,tid = 1,date_time = datetime.datetime.now(),status = "Completed",rescode = 2,type_trans = "Cash Withdrawal",amt_with = Decimal(request.POST['amount']),cur_bal=t_acc.balance)
			t.save()
			wdmessage = 1
			request.session.flush()
		else:
			ta = Cash_Withdrawl(atmcard_num_id = request.session['cardnumber'], machine_id_id =1, tid = 1, date_time = datetime.datetime.now(),status = "Not Completed",rescode = 11,type_trans = "Cash Withdrawal",amt_with = Decimal(request.POST['amount']),cur_bal = t_acc.balance)
			ta.save()
			wdmessage = 2
	return render_to_response('finale/cashwithdrawal.html', locals())

@csrf_protect	
def cashtransfer(request):
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')
	username=request.session['username']
	if request.method == 'POST':
		accnum = request.POST['acc_num']
		accname = request.POST['name']
		print accnum
		#acc_2 = Account_Ext.objects.get(acc_num=str(accnum),name=str(accname))
		acc_2 = Account_Ext.objects.filter(acc_num=accnum,name=accname)
		if not acc_2:
			ctmessage = 0
		else:
			atmcard = ATM_Card.objects.get(atmcard_num=request.session['cardnumber'])
			t_acc = Account_Ext.objects.get(acc_num=str(atmcard.account_num))
			if(Decimal(t_acc.balance)>Decimal(request.POST['amount'])):
				t_acc.balance = t_acc.balance - Decimal(request.POST['amount'])
				t_acc.save()
				acc_2[0].balance = acc_2[0].balance + Decimal(request.POST['amount'])
				acc_2[0].save()
				t = Cash_Transfer(atmcard_num_id = request.session['cardnumber'], machine_id_id = 1,tid = 1,date_time = datetime.datetime.now(),status = "Completed",rescode = 3,type_trans = "Cash Transfer",amt_trans = Decimal(request.POST['amount']),ben_acc_num=accnum,ben_name=accname)
				t.save()
				ctmessage = 1
				request.session.flush()
			else:
				ta = Cash_Transfer(atmcard_num_id = request.session['cardnumber'], machine_id_id =1, tid = 1, date_time = datetime.datetime.now(),status = "Not Completed",rescode = 12,type_trans = "Cash Transfer",amt_trans = Decimal(request.POST['amount']),ben_acc_num=accnum,ben_name=accname)
				ta.save()
				ctmessage = 2
				request.session.flush()		
	
	return render_to_response('finale/cashtransfer.html', locals())

@csrf_protect
def pinchange(request):
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')
	username = request.session['username']
	if request.method == 'POST':
		atmcard = ATM_Card.objects.get(atmcard_num=request.session['cardnumber'])
		cardpin = request.POST['pincode']
		npin = request.POST['npincode']
		cpin = request.POST['cpincode']
		if int(atmcard.pin) == int(cardpin):
			if int(npin) == int(cpin):
				if int(atmcard.pin) == int(cpin):
					#same no need to do any thing
					pcmessage=1
				else:
					#successfull
					pcmessage=4
					t = Pin_change(atmcard_num_id = request.session['cardnumber'], machine_id_id = 1,tid = 1,date_time = datetime.datetime.now(),status = "Completed",rescode = 4,type_trans = "Pin Change",prev_pin=cardpin,new_pin=npin)
					t.save()
					atmcard.pin=int(cpin)
					atmcard.save() 
						
			else:
				#new pin and confirm pin are different
				pcmessage=2
			
		else:
			#invalid pincode
			pcmessage=3
	return render_to_response('finale/pinchange.html', locals())

@csrf_protect	
def phonechange(request):
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')
	username = request.session['username']
	if request.method == 'POST':
		atmcard = ATM_Card.objects.get(atmcard_num=request.session['cardnumber'])
		nphone = request.POST['nphone']
		cphone = request.POST['cphone']
		if int(nphone) == int(cphone):
				if int(atmcard.phone_num) == int(cphone):
					#same no need to do any thing
					pcmessage=1
				else:
					#successfull
					pcmessage=4
					t = Phone_change(atmcard_num_id = request.session['cardnumber'], machine_id_id = 1,tid = 1,date_time = datetime.datetime.now(),status = "Completed",rescode = 4,type_trans = "Pin Change",prev_phone=atmcard.phone_num,new_phone=nphone)
					t.save()
					atmcard.phone_num=int(cphone)
					atmcard.save() 
						
		else:
			#new phoneno and confirm phoneno are different
			pcmessage=2
	return render_to_response('finale/phonechange.html', locals())

@csrf_protect	
def fastcash(request):
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')
	username=request.session['username']
	if request.method == 'POST':
		atmcard = ATM_Card.objects.get(atmcard_num=request.session['cardnumber'])
		t_acc = Account_Ext.objects.get(acc_num=str(atmcard.account_num))
		if(Decimal(t_acc.balance)>Decimal(request.POST['fcash'])):
			t_acc.balance = t_acc.balance - Decimal(request.POST['fcash'])
			t_acc.save()
			t = Cash_Withdrawl(atmcard_num_id = request.session['cardnumber'], machine_id_id = 1,tid = 1,date_time = datetime.datetime.now(),status = "Completed",rescode = 2,type_trans = "Cash Withdrawal",amt_with = Decimal(request.POST['fcash']),cur_bal=t_acc.balance)
			t.save()
			fcmessage = 1
			request.session.flush()
		else:
			ta = Cash_Withdrawl(atmcard_num_id = request.session['cardnumber'], machine_id_id =1, tid = 1, date_time = datetime.datetime.now(),status = "Not Completed",rescode = 11,type_trans = "Cash Withdrawal",amt_with = Decimal(request.POST['fcash']),cur_bal = t_acc.balance)
			ta.save()
			fcmessage = 2
	return render_to_response('finale/fastcash.html', locals())
	
@csrf_protect
def exit(request):
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')
	request.session.flush()
	return redirect('/user')

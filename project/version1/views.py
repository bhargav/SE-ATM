# Create your views here.
from version1.models import Admin
from version1.models import Account_Ext
from version1.models import ATM_Card
from version1.models import Balance_Enquiry
from version1.models import Transaction
from version1.models import Machine
from version1.models import Cash_Withdrawl
from version1.models import Cash_Transfer
from decimal import *
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404 
import datetime

def admin_index(request):
    Admin_list = Admin.objects.all()
    #print Admin_list
    return render_to_response('admin_user/index.html', locals())

def admin_verify_user(request):
	global login
	[admin]=Admin.objects.filter(Admin_id=request.GET['username'],Password=request.GET['password'])
	if admin:
		login=True
		return render_to_response('admin_user/main_page.html',{"login":login})# locals())
	else:
		Admin_list = Admin.objects.all()
		return render_to_response('admin_user/index.html', locals())
		
def admin_main_page(request):
	global login
	return render_to_response('admin_user/main_page.html', {"login":login})#locals())
##################################### admin : add new card ######################################
def admin_add_card(request):
	global login
	return render_to_response('admin_user/main_page.html', {"login":login})#locals())
##################################### admin : atm status ##########################################
def admin_atm_status(request):
	global login
	#[Machine]=Machine.objects.all()
	Machine_list = Machine.objects.all()
	return render_to_response('admin_user/view_atm_status.html', {"Machine_list":Machine_list})	
	
def admin_update_refill(request):
	global login
	[machine] =Machine.objects.filter(machine_id=request.GET['id'])
	date_time = datetime.datetime.now()
	machine.next_maintainence_date=date_time
	machine.save()
	Machine_list = Machine.objects.all()
	return render_to_response('admin_user/view_atm_status.html', {"Machine_list":Machine_list})
#################################### admin : update card details #####################################
def admin_update_card_details(request):
	global login
	return render_to_response('admin_user/enter_card_no.html', {"login":login})#locals())	

def admin_card_validation(request):
	global admin_session_card
	global admin_session
	global login
	p = get_object_or_404(Account_Ext, pk=request.GET['cardnumber'])
	date=datetime.datetime.now()
	[cardcheck] =ATM_Card.objects.filter(atmcard_num=request.GET['cardnumber'])
	if(cardcheck.expiry_date > date):
		print cardcheck.expiry_date
		print date
		card=cardcheck
		admin_session_card = request.GET['cardnumber']
		admin_session=True
		return render_to_response('admin_user/update_card_details.html', {"login":login})
	return HttpResponse("CARD IS EXPIRED")
	
def	admin_update_card_main_page(request):
	global login
	global admin_session
	if (admin_session):
		return render_to_response('admin_user/update_card_details.html', {"login":login})
	else:
		return render_to_response('admin_user/enter_card_no.html', {"login":login})
	
def admin_block_card(request):
	global login
	global admin_session
	if (admin_session):
			return render_to_response('admin_user/block_card.html', {"login":login})
	else:
		return render_to_response('admin_user/enter_card_no.html', {"login":login})
	
def admin_block_card_operation(request):
	global login
	global admin_session
	global admin_session_card
	if (admin_session):
		[cardcheck] =ATM_Card.objects.filter(atmcard_num=admin_session_card)
		cardcheck.card_status=False
		cardcheck.save()
		return render_to_response('admin_user/update_card_details.html', {"login":login})
	else:
		return render_to_response('admin_user/enter_card_no.html', {"login":login})


def admin_activate_card(request):
	global login
	global admin_session
	if (admin_session):
			return render_to_response('admin_user/activate_card.html', {"login":login})
	else:
		return render_to_response('admin_user/enter_card_no.html', {"login":login})
	
def admin_activate_card_operation(request):
	global login
	global admin_session
	global admin_session_card
	if (admin_session):
		[cardcheck] =ATM_Card.objects.filter(atmcard_num=admin_session_card)
		cardcheck.card_status=False
		cardcheck.save()
		return render_to_response('admin_user/update_card_details.html', {"login":login})
	else:
		return render_to_response('admin_user/enter_card_no.html', {"login":login})
	
def admin_reset_pincode(request):
	global login
	return render_to_response('admin_user/reset_pin.html', {"login":login})

def admin_reset_pincode_operation(request):
	global login
	global admin_session
	global admin_session_card
	if (admin_session):
		[cardcheck] =ATM_Card.objects.filter(atmcard_num=admin_session_card)
		cardcheck.pin=request.GET['password1']
		cardcheck.save()
		return render_to_response('admin_user/update_card_details.html', {"login":login})
	else:
		return render_to_response('admin_user/enter_card_no.html', {"login":login})

def admin_reset_phone(request):
	global login
	return render_to_response('admin_user/reset_phone.html', {"login":login})

def admin_reset_phone_operation(request):
	global login
	global admin_session
	global admin_session_card
	if (admin_session):
		[cardcheck] =ATM_Card.objects.filter(atmcard_num=admin_session_card)
		cardcheck.phone_num=request.GET['phone1']
		cardcheck.save()
		return render_to_response('admin_user/update_card_details.html', {"login":login})
	else:
		return render_to_response('admin_user/enter_card_no.html', {"login":login})	
	
def admin_view_history(request):
	global login
	return render_to_response('admin_user/view_history.html', {"login":login})

def admin_update_date(request):
	global login
	return render_to_response('admin_user/update_expiring_date.html', {"login":login})

def admin_update_date_operation(request):
	global login
	global admin_session
	global admin_session_card
	if (admin_session):
		[cardcheck] =ATM_Card.objects.filter(atmcard_num=admin_session_card)
		#cardcheck.phone_num=request.GET['date']
		#cardcheck.save()
		return render_to_response('admin_user/update_card_details.html', {"login":login})
	else:
		return render_to_response('admin_user/enter_card_no.html', {"login":login})	
##########################################################################################################################
def index(request):
    Account_holder_list = Account_Ext.objects.all()
    return render_to_response('version1/index.html', locals())

def validatecard(request):
	global session
	p = get_object_or_404(Account_Ext, pk=request.GET['cardnumber'])
	date=datetime.datetime.now()
	[cardcheck] =ATM_Card.objects.filter(atmcard_num=request.GET['cardnumber'],card_status=True)
	if(cardcheck.expiry_date > date):
		print cardcheck.expiry_date
		print date
		card=cardcheck
		session = request.GET['cardnumber']
		return render_to_response('version1/pincode.html', locals())
	return HttpResponse("CARD IS EXPIRED")	
    
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

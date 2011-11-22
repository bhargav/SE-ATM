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
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

# admin_index() is the index page of the administrator where he will be asked to fill the 
# user name and password 
@csrf_protect
def admin_index(request):    
    return render_to_response('admin_user/index.html', locals())
    
    
# admin_verify_user() user will verify the administrator and password entered by him
# this function starts the session for the Administrator if username and password are entered correctly      
@csrf_protect
def admin_verify_user(request):
	admin=Admin.objects.filter(Admin_id=request.GET['username'],Password=request.GET['password'])
	if not admin:
		failed=True
		return render_to_response('admin_user/index.html', {"failed":failed})#locals())
	else:	 	
		request.session['login'] = True
		return render_to_response('admin_user/main_page.html',locals())
		
		
# admin_main_page() displays all the option for the administrator  		
def admin_main_page(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		return render_to_response('admin_user/main_page.html', locals())
		
		
##################################### admin : add new card ######################################
# admin_add_card() adds a new ATM card for the customer
def admin_add_card(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		return render_to_response('admin_user/main_page.html', {"login":login})#locals())
##################################### admin : atm status ##########################################
# admin_atm_status() will show the details of all the ATM-machines 
def admin_atm_status(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		Machine_list = Machine.objects.all()
		return render_to_response('admin_user/view_atm_status.html', {"Machine_list":Machine_list})	

# admin_update_refill() will send a request to the autority to fill the refill of that ATM machine		
def admin_update_refill(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		[machine] =Machine.objects.filter(machine_id=request.GET['id'])
		date_time = datetime.datetime.now()
		machine.next_maintainence_date=date_time
		machine.save()
		Machine_list = Machine.objects.all()
		return render_to_response('admin_user/view_atm_status.html', {"Machine_list":Machine_list})
#################################### admin : update card details #####################################
# admin_update_card_details will ask the administrator to enter the atm card number which he want to update
def admin_update_card_details(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		return render_to_response('admin_user/enter_card_no.html', locals())	
# admin_card_validation() will validate the atm card no and it is correct then it will take the administrator to options
# else it will dispay that card is not valid
def admin_card_validation(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		cardcheck =ATM_Card.objects.filter(atmcard_num=request.GET['cardnumber'])
		if not cardcheck:
			failed=True
			return render_to_response('admin_user/enter_card_no.html', {"failed":failed})	
		else:			 	
			card=cardcheck
			request.session['admin_session_card'] = request.GET['cardnumber']
			request.session['admin_session']=1
			return render_to_response('admin_user/update_card_details.html', locals())
			
		
# admin_update_card_main_page() displays all the options on the screen for the administrator too update the card details		
def	admin_update_card_main_page(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:			
			return render_to_response('admin_user/update_card_details.html', locals())
			
# admin_block_card() asks of the confirmation from the administrator to block the ATM card 		
def admin_block_card(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:			
			return render_to_response('admin_user/block_card.html', locals())

# admin_block_card() block the ATM card		
def admin_block_card_operation(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:			
			[cardcheck] =ATM_Card.objects.filter(atmcard_num=request.session['admin_session_card'])
			cardcheck.card_status=False
			cardcheck.save()
			return render_to_response('admin_user/update_card_details.html', locals())	
			
# admin_activate_card() asks of the confirmation from the administrator to activate the ATM card	
def admin_activate_card(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:			
			return render_to_response('admin_user/activate_card.html', locals())	
		
# admin_activates_card() activates the ATM card		
def admin_activate_card_operation(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:			
			[cardcheck] =ATM_Card.objects.filter(atmcard_num=request.session['admin_session_card'])
			cardcheck.card_status=True
			cardcheck.save()
			return render_to_response('admin_user/update_card_details.html', locals())	
			
# admin_reset_pincode()	aks the administrator to enter the new pin		
def admin_reset_pincode(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:			
			return render_to_response('admin_user/reset_pin.html', locals())	
			
# admin_reset_pincode_operation() reset the pin to new pin enetered by the administrator			
def admin_reset_pincode_operation(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:
			if ((request.GET['password1']=="") or (request.GET['password2']=="")):
				empty=True 
				return render_to_response('admin_user/reset_pin.html', {"empty":empty})		
			else:
				if (request.GET['password1']==request.GET['password2']):			
					[cardcheck] =ATM_Card.objects.filter(atmcard_num=request.session['admin_session_card'])
					cardcheck.pin=request.GET['password1']
					cardcheck.save()
					return render_to_response('admin_user/update_card_details.html', locals())	
				else:
					match=True 
					return render_to_response('admin_user/reset_pin.html', {"match":match})

# admin_reset_phone()	aks the administrator to enter the new phone			
def admin_reset_phone(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:			
			return render_to_response('admin_user/reset_phone.html', locals())	

# admin_reset_phone_operation() reset the phone to new phone enetered by the administrator			
def admin_reset_phone_operation(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:
			if ((request.GET['phone1']=="") or (request.GET['phone2']=="")):
				empty=True 
				return render_to_response('admin_user/reset_phone.html', {"empty":empty})		
			else:
				if (request.GET['phone1']==request.GET['phone2']):			
					[cardcheck] =ATM_Card.objects.filter(atmcard_num=request.session['admin_session_card'])
					cardcheck.phone_num=request.GET['phone1']
					cardcheck.save()
					return render_to_response('admin_user/update_card_details.html', locals())	
				else:
					match=True 
					return render_to_response('admin_user/reset_phone.html', {"match":match})	
				 
				
# admin_view_history() shows the previous history of the ATM card 					
def admin_view_history(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:			
			return render_to_response('admin_user/view_history.html', locals())	
			
# admin_update_date() reset the expiring date of the ATM card to further 4 years			
def admin_update_date(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:			
			return render_to_response('admin_user/update_expiring_date.html', locals())
			
# admin_update_date_operation() update the expiring date in the database		
def admin_update_date_operation(request):
	if 'login' not in request.session:
		return render_to_response('admin_user/index.html', locals())
	else:
		if 'admin_session' not in request.session:
			return render_to_response('admin_user/enter_card_no.html', locals())
		else:							
			[cardcheck] =ATM_Card.objects.filter(atmcard_num=request.session['admin_session_card'])
			#cardcheck.phone_num=request.GET['date']
			#cardcheck.save()
			return render_to_response('admin_user/update_card_details.html', locals())	
	
##########################################################################################################################
def index(request):
    Account_holder_list = Account_Ext.objects.all()
    return render_to_response('version1/index.html', locals())

def validatecard(request):
	global session
	p = get_object_or_404(Account_Ext, pk=request.GET['cardnumber'])
	date=datetime.datetime.now()
	cardcheck =ATM_Card.objects.filter(atmcard_num=request.GET['cardnumber'],card_status=True)
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

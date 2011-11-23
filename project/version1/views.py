# Create your views here.
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
	'''It displays the main page which includes the form which validates the cardnumber'''
	if 'cardnumber' in request.session:
		return redirect('/user/validatepin/')  
		
	if request.method == 'POST':
		cardnum = request.POST['cardnumber']
		card = ATM_Card.objects.filter(atmcard_num=cardnum)
		if not card:
			cmessage=1
		elif not card[0].card_status:
			cmessage=2
		else:
			date = datetime.datetime.now()
			if(card[0].expiry_date < date):
				cmessage=3
			else:
				request.session['cardnumber'] = cardnum  
				return redirect('/user/validatepin/')   
	return render_to_response('finale/index.html',locals())   

@csrf_protect
def validatepin(request):
	'''It displays the page which includes the form which validates the user based on pincode if card is already verified'''
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
			request.session.set_expiry(300)
			return redirect('/user/options')
		if 'pinattempt' not in request.session:
			request.session['pinattempt'] = 1
		else:
			request.session['pinattempt'] = request.session['pinattempt'] + 1
		
		if request.session['pinattempt'] == 1:
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
	'''displays the options available if user has been verified'''
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')
	print request.session.get_expiry_age()
	username = request.session['username']
	return render_to_response('finale/options.html', locals())

@csrf_protect
def balanceenquiry(request):
	'''it displays the balance of card holder if he is already been verified'''
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
	'''It displays the page in which user can enter the amount and if user has entered the amount then transaction is saved in database based on status(COMPLETED OR NOT) '''
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
	'''It displays the page in which user can enter the amount,account,name and if user has entered the cash transfer details then transaction is saved in database based on status(COMPLETED OR NOT) '''
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
	'''It displays the page in which user has the privelege to change his/her pincode'''
	
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
	'''It displays the page in which user has the privelege to change his/her phoneno'''
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
	'''It displays the page in which user can choose the amount listed in four options and the transaction is saved in database based on status(COMPLETED OR NOT) '''
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
	'''To delete the session and take out the card'''
	if 'cardnumber' not in request.session:
		return redirect('/user/')
	if 'pinverified' not in request.session:
		return redirect('/user/pinvalidation/')
	request.session.flush()
	return redirect('/user')

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

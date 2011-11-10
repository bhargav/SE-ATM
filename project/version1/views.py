# Create your views here.
from version1.models import Account_Ext
from version1.models import ATM_Card
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404 
session=0
def index(request):
    Account_holder_list = Account_Ext.objects.all()
    return render_to_response('version1/index.html', locals())

def validatecard(request):
	global session
	p = get_object_or_404(Account_Ext, pk=request.GET['cardnumber'])
	session = p
	return render_to_response('version1/pincode.html', locals())
    
def validatepin(request):
    #Account_holder_list = Account_Ext.objects.all()
    global session
    pin = ATM_Card.objects.filter(pin=request.GET['pincode'],atmcard_num=session.atmcard_num)
    if pin:
		return HttpResponse("Your pincode is valid")	
    return HttpResponse("Your pincode is not valid")

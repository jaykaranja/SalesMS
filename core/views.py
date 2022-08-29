import datetime
import random
import string
from time import timezone
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from core.forms import PaymentItemForm
from .models import Payment, PaymentItem, Product

# Create your views here.

class Authentication:
    def loginuser(request):
        if request.method =="POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is None:
                message  = 'Invalid login details'
                context = {
                    'message' : message, 
                }
                return render(request, 'core/login.html', context)
            login(request, user)
            return redirect('dashboard')
        return render(request, 'core/login.html')
    
    def logoutuser(request):
        logout(request)
        return redirect('login')
    
    
    
class Dashboard:
    @login_required()
    def dashboard(request):
        user = request.user
        context = {
            'user' : user,
        }
        return render(request, 'core/dashboard.html', context)

    @login_required()
    def products(request):
        products = Product.objects.all()
        context = {
            'products' : products,
        }
        return render(request, 'core/products.html', context)
        
    @login_required()
    def checktodayspayments(request):
        todayspayments = Payment.objects.filter(date_created__date = datetime.date.today())
        context = {
            'todayspayments' : todayspayments,
        }
        return render(request, 'core/paymentstoday.html', context)
    
    @login_required()
    def enterpayment(request):
        return render(request, 'core/enterpayment.html')
    
    def create_random_number():
        return ''.join(random.choices(string.digits, k=6))
    
        
    @login_required()
    def createpayment(request):
        random_id = ''.join(random.choices(string.digits, k=6))
        try:
            payment = Payment.objects.create(payment_id = random_id, authorized_by = request.user)
        except IntegrityError:
            payment = Payment.objects.create(payment_id = random_id, authorized_by = request.user)

        
        return redirect('payment-item-entry', args=payment.payment_id)
    
    @login_required()
    def payment_item_entry(request, args):
        try: 
            payment = get_object_or_404(Payment, payment_id=args)
            
        except ObjectDoesNotExist:
            context = {
            'message' : f"'Payment doesn't exist'",
            'messagetype' : 'danger',
            }
            return render(request, 'core/enterpayment.html', context)
        
        if payment.confirmed is True:
            context = {
            'message' : 'Payment already submitted',
            'messagetype' : 'danger',
            }
            return render(request, 'core/enterpayment.html', context)
        
        paymentitems = payment.paymentitem_set.all()
        if request.method == "POST":
            form = PaymentItemForm(request.POST or None)
            paymentitem = form.save(commit=False)
            paymentitem.payment = payment
            paymentitem.save()
            return redirect('payment-item-entry', args=payment.payment_id)
        
        form = PaymentItemForm       
        context = {
            'payment' : payment,
            'form' : form,
            'items' : paymentitems,
        }
        return render(request, 'core/enterpayment.html', context)
    
    @login_required()
    def confirmpayment(request, args):
        payment = get_object_or_404(Payment, payment_id=args)
        payment.confirmed = True
        payment.save()
        context = {
            'message' : 'Payment submitted successfully',
            'messagetype' : 'success',
        }
        
        return render(request, 'core/enterpayment.html', context)
    
    @login_required()
    def paymentview(request, id):
        payment = get_object_or_404(Payment, payment_id=id)
        items = payment.paymentitem_set.all()
        context = {
            'payment' : payment,
            'items' : items,
        }
        return render(request, 'core/paymentstoday.html', context)
    

    @login_required()
    def deletepaymentitem(request, id, args):
        paymentitem = PaymentItem.objects.get(pk=id)
        paymentitem.delete()
        return redirect('payment-item-entry', args=args)


    @login_required()
    def querypaymentbyid(request):
        if request.method == "POST":
            paymentid = request.POST['id']
            try:
                payment = Payment.objects.get(payment_id=paymentid)
                items = payment.paymentitem_set.all()
                context = {
                    'payment' : payment,
                    'items' : items,
                }
                return render(request, 'core/querypaymentbyid.html', context)
                
            except ObjectDoesNotExist:
                context = {
                    'message' : 'Payment does not exist. Please try again.',
                }
                return render(request, 'core/querypaymentbyid.html', context)
        return render(request, 'core/querypaymentbyid.html')
        



    



class Adminapp():
    """
    If user tries to log in to admin as normal user
    """
    def loginasadminerror(request):
        if request.method =="POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is None:
                message  = 'Invalid login details'
                context = {
                    'message' : message, 
                }
                return render(request, 'core/login.html', context)        
            login(request, user)
            return redirect('admin-index')

        context = {
            'message' : f"Sorry, you're not an administrator.",
        }
        return render(request, 'core/login.html', context)
    

    @permission_required(perm='is_superuser is True', login_url='loginasadminerror')
    def index(request):
        users = User.objects.all()
        
        def todaystotals():
            total = 0
            todayssales = Payment.objects.filter(date_created__date =datetime.date.today())
            for sale in todayssales:
                total = sale.total_price() + total
            return total
                    
        def monthstotals(): 
            total = 0
            monthsales = Payment.objects.filter(date_created__date = datetime.date.today() - datetime.timedelta(30))
            for sale in monthsales:
                total = sale.total_price() + total
            
            return total

        context = {
            'users' : users,
            'todayssales' : todaystotals,
            'monthsales' : monthstotals,
        }
        return render(request, 'adminapp/index.html', context)
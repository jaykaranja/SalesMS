from django.urls import path
from .views import Authentication, Dashboard, Adminapp

urlpatterns = [
    path('login', Authentication.loginuser, name='login'),
    path('logout', Authentication.logoutuser, name='logout'),
    path('', Dashboard.dashboard, name='dashboard'),
    path('payment', Dashboard.enterpayment, name='enterpayment'),
    path('payments-today', Dashboard.checktodayspayments, name='payments-today'),
    path('products', Dashboard.products, name='products'),
    path('create-payment', Dashboard.createpayment, name='create-payment'),
    path('payment-items/<int:args>', Dashboard.payment_item_entry, name='payment-item-entry'),
    path('confirmpayment/<int:args>', Dashboard.confirmpayment, name='confirmpayment'),
    path('paymentview/<int:id>', Dashboard.paymentview, name='paymentview'),
    path('payment-items/<int:args>/<int:id>', Dashboard.deletepaymentitem, name='delete-payment-item'),
    path('querypaymentbyid', Dashboard.querypaymentbyid, name='querypaymentbyid'),
    path('administration/', Adminapp.index, name='admin-index'),
    path('loginasadminerror', Adminapp.loginasadminerror, name='loginasadminerror'),
    path('administration/paymentview/<int:id>', Adminapp.viewpayment, name='adminpaymentview')
]

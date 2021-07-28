from django.contrib import messages
from django.utils.safestring import mark_safe
import json

from django.http import response
from .functions import send_request
from os import path
from django.http.response import Http404, JsonResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from .models import Order, Payouts, Refunds, User
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import razorpay
import random

rname = "rzp_test_jYvNsa4FusIMK5"
rpass = "s6Vo8mE40GB2ZZlZmgNTlDwE"


def index(request):
    return render(request, 'payments/index.html')


client = razorpay.Client(auth=(rname, rpass))


def payment(request):
    callback_url = 'http://' + str(get_current_site(request))+"/handlerequest/"
    if request.method == 'POST':
        user_to = request.POST.get('user_to')
        user_from = request.POST.get('user_from')
        amount = int(request.POST.get('amount'))

        order = Order()
        order.order_id = random.randint(99999, 999999)
        order.user_id = user_from
        order.to_user_id = user_to
        order.amount = int(amount)
        order.save()
        rpay_order = client.order.create(
            {'amount': amount*100, 'currency': "INR", 'receipt': str(order.order_id), 'payment_capture': 0})
        order.razorpay_order_id = rpay_order.get('id')
        order.save()
        context = {
            'order': order,
            'order_id': rpay_order['id'],
            'orderId': order.order_id,
            'final_price': amount, 'razorpay_merchant_id': 'rzp_test_jYvNsa4FusIMK5',
            'callback_url': callback_url
        }
        print(context)
        return render(request, 'payments/pay.html', context)
    else:
        return Http404()


@csrf_exempt
def verifyPayment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        order = Order.objects.get(
            razorpay_order_id=request.POST.get('razorpay_order_id'))
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature
        order.save()
        result = client.utility.verify_payment_signature(params_dict)
        if result == None:
            order.payment_status = 'success'
            order.save()
            return JsonResponse({'status': 'payment completed successfully'})
        order = Order.objects.get(
            razorpay_order_id=request.POST.get('razorpay_order_id'))
        order.payment_status = 'failure'
        order.save()
        return JsonResponse({'status': 'unfortunately payment got failed'}, safe=False)


    else:
        return JsonResponse({'error': 'invalid request'})


def completed(request):
    context = {
        'orders':Order.objects.filter(payment_status='success')
    }

    return render(request,'payments/completed.html',context)
    
def refund(request,payid):

    if request.method=='POST':
        amount = float(request.POST.get('amount',0))
        amount = int((amount*100))
        print('amount',amount)
        try:
            client.payment.capture(payid, amount)
        except:
            pass
        try:
            
        
            order = Order.objects.get(razorpay_payment_id=payid)
            x = client.payment.refund(payid, amount)
            order.payment_status = 'refunded'
            order.save()
            Refunds.objects.create(order_id =order.pk,refund_id = x['id'] )

        except Exception as e:
            return JsonResponse({'error': True, 'message': str(e)})
        return JsonResponse({'error': False, 'message': "refund processed successfully",'respose':x})
    return JsonResponse({'error':True,'message':'invalid request'})


def create_contacts(request, pk):
    try:
        _user = User.objects.get(id=pk)
    except:
        return JsonResponse({'error': True, 'message': 'invalid user id'})
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('phno')
        payloa = json.dumps(
            {
                "name": name,
                "email": email,
                "contact": contact.strip('+'),
                "type": "vendor",
                "reference_id": "Acme Contact ID 12345"
            }
        )
        x = send_request(path='contacts', auth={
            'username': rname, 'password': rpass}, payload=payloa)

        try:
            _user.shopprofile.contact_id = x['id']
            _user.shopprofile.save()
            messages.success(request, mark_safe(
                'your account has been successfully created'))
        except:

            return JsonResponse(x)
    return render(request, "payouts/contact.html", context={'user': _user})



def create_fund_account(request, id):
    try:
        _user = User.objects.get(id=id)
    except:
        return JsonResponse({'error': True, 'message': 'invalid user id'})
    # print()
    if request.method == 'POST':

        name = request.POST.get('name')
        ifsc = request.POST.get('ifsc')
        acno = request.POST.get('acno')
        payloa = json.dumps(
            {
                "contact_id": _user.shopprofile.contact_id,
                "account_type": "bank_account",
                "bank_account": {
                    "name": str(name),
                    "ifsc": str(ifsc),
                    "account_number": str(acno)
                }
            }
        )

        x = send_request(path='fund_accounts', auth={
            'username': rname, 'password': rpass}, payload=payloa)
        try:

            _user.shopprofile.fund_id = x['id']
            _user.shopprofile.save()
            messages.success(request, mark_safe(
                'your fund account has been successfully created'))
        except:

            return JsonResponse(x)

    return render(request, 'payouts/index.html', context={'user': _user})


def create_payout(request, id):
    try:
        _user = User.objects.get(id=id)
    except:
        return JsonResponse({'error': True, 'message': 'invalid user id'})
    if request.method == "POST":
        amount = int(request.POST.get('amount', 0))
        comm = float(request.POST.get('comm', 0))/100
        print(comm)
        # amount = int(sum([i.amount for i in Order.objects.filter(to_user_id=id)]))
        total = amount-(amount*comm)
        payloa = json.dumps(
            {
                "account_number": "2323230065002309",
                "fund_account_id": _user.shopprofile.fund_id,
                "amount": int(total)*100,
                "currency": "INR",
                "mode": "IMPS",
                "purpose": "payout",
                "queue_if_low_balance": True,
            }
        )
        x = send_request(path='payouts', auth={
            'username': rname, 'password': rpass}, payload=payloa)
        try:
            Payouts.objects.create(p_id=x['id'], amount=amount, paid_amount=total, commission=(
                amount*comm), user_id=_user.pk)
            messages.success(request, mark_safe(
                'your payout has been successfully created'))
        except:

            return JsonResponse({'error': x})
    return render(request, 'payouts/payout.html', context={'user': _user})

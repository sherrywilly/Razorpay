from django.http import response
from django.http.response import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import razorpay
import hmac
import hashlib
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, Transaction

rname = "rzp_test_hkwOy4WY561PNE"
rpass = "rzp_test_hkwOy4WY561PNE"

client = razorpay.Client(auth=(rname, rpass))

# @csrf_exempt
# def VerifyPayHook(request):
    # jsondata = request.body
    # print(jsondata)
    # data  = json.loads(jsondata)
    # data = json.dumps(request.body, separators=(',', ':'))
    # print(data)
    # key = 'sherry'
    # signature = request.headers['X-Razorpay-Signature']
    # print(request.headers)
    # yy = hamc.new()
    # try:
    #     x = client.utility.verify_webhook_signature(str(data), signature, key)
    #     print(x)
    # except Exception as e:
    #     print(e)
        # pass
   
#     signature = hmac.new(
#    bytes(key, 'utf-8'),
#     msg=bytes(jsondata, 'utf-8'),
#     digestmod=hashlib.sha256)
#     generated_signature = signature.hexdigest()
    # return JsonResponse({'status':'ok'})

class VerifyPayHook(APIView):
    def post(self,request):
        # print(request.data)
        webhook_secret: str  = 'sherry'
        payload = request.data
        payload_body = json.dumps(request.data, separators=(',', ':'))
        signature=request.headers['X-Razorpay-Signature']
        print(signature);
        # with open('readme.json','w') as f:
        #     f.write(json.dumps(request.data,indent=2))
        try:
            verify = client.utility.verify_webhook_signature(payload_body, signature, webhook_secret)
            # ! it will exit  if not verified it will raise an error 
            if payload['event']=='refund.processed':
                print('refund initiated')
                _x=payload['payload']['refund']
                print(_x['entity']['id'])
                order = Order.objects.get(razorpay_order_id=_x['entity']['id'])
                
                order.payment_status = 'refunded'
                order.save()
                trans = Transaction()
                trans.order =order
                trans.response = payload
                trans.refund_id =_x['entity']['id']
                trans.r_pay_id =_x['entity']['payment_id']
                trans.hook_signature =signature
                trans.save()

            elif payload['event']=='payment.captured':
                print('payment captured')
                _x=payload['payload']['payment']
                print(_x['entity']['order_id'])
                order = Order.objects.get(razorpay_order_id=_x['entity']['order_id'])
                
                order.payment_status = 'success'
                order.save()
                trans = Transaction()
                trans.order =order
                trans.response = payload
                trans.r_order_id =_x['entity']['order_id']
                trans.r_pay_id =_x['entity']['id']
                trans.hook_signature =signature
                trans.save()
            elif payload['event'] == 'payout.created':
                print('payout created')


            elif payload['event'] =='payout.failed':
                print('payment failed')
                _x=payload['payload']['payment']
                print(_x['entity']['order_id'])
                order = Order.objects.get(razorpay_order_id=_x['entity']['order_id'])
                order.payment_status = 'failure'
                order.save()
                trans = Transaction()
                trans.order =order
                trans.response = payload
                trans.r_order_id =_x['entity']['order_id']
                trans.r_pay_id =_x['entity']['id']
                trans.hook_signature =signature
                trans.save()
            else:
                raise ValueError
        except Exception as e:
            print(e)
            print('----------------')
        return Response({'test':'ok'})


from django.urls import path
from .views import completed, create_contacts, create_fund_account, create_payout, index,payment, refund,verifyPayment
from .webhooks import VerifyPayHook
urlpatterns = [
    path('',index,name="index"),
    
    path('payment/continue/',payment,name="pay"),
    path('handlerequest/',verifyPayment,name="verify"),
    path('payment/<payid>/refund/',refund,name="refund"),
    path('payments',completed),
    # path('payment/refund/',refund,name="refund"),
    path('payouts/<int:pk>/add_contact/',create_contacts,name="create"),
    path('payouts/<int:id>/add_bank/',create_fund_account,name="create_bank"),
    path('payouts/<int:id>/pay/',create_payout,name="create"),
    # path('payouts/<int:id>/pay/',create_payout,name="create"),


    #####################!--------------  HOOK URLS ----------------##########################
    path('hooks/verify/',VerifyPayHook.as_view()),
    # path('hooks/verify/refund/',VerifyRefundHook.as_view())
]

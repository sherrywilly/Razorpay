from django.http.response import JsonResponse
from django.views.generic import View

class VerifyPayHook(View):
    def get(self,request):
        return JsonResponse({'error':True,"message":'invalid accces'})

    def post(self,request):
        pass
from django.shortcuts import render, HttpResponse, Http404
import json
import datetime
from django.utils import timezone
from django.http import HttpResponseBadRequest
from .forms import EmailForm
from accounts.models import EmailMarketingSignUp
# Create your views here.

def dismiss_marketing_message(request):
    if request.is_ajax():
        data = {"success":True,}
        json_data = json.dumps(data)
        request.session['dismiss_message_for'] = str(timezone.now() + datetime.timedelta(hours=3))
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404
    
def email_signup(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_signup = EmailMarketingSignUp.objects.get_or_create(email=email)
            request.session['email_added_marketing'] = True
            return HttpResponse("Sucess %s" % email)
        if form.errors:
            json_data = json.dumps(form.errors)
            return HttpResponseBadRequest(json_data, content_type="application/json")
        else:
            raise Http404
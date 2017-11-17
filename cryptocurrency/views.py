from django.http import HttpResponse
from cryptocurrency import handler
from django.template import Template, loader, Context
from django.shortcuts import redirect
import urllib2, urllib


def home(request):
    return HttpResponse("<h3>Your app is working</h3>")


def test(request):
    return HttpResponse("<h3>This is a test page<h3>")


def static_content(request):
    return HttpResponse("<p>This is a static content</p>")


def json_response(request):
    return HttpResponse("{'url':'" + str(request.path_info) + "','isSucess':'true'}")


def collections(request):
    if request.POST:
        handler.write_collections(request.POST)
    return HttpResponse(handler.read_collections('all'))


def post_request(request):
    request1 = urllib2.Request("https://www.zebapi.com/api/v1/market/ticker/btc/inr")
    respone = urllib2.urlopen(request1)
    print respone.read()


def rates(request):
    currency = request.GET['currency'] if request.GET.__contains__('currency') == '' else 'inr'
    print currency
    updates = handler.update_crypto_currency_rates(currency)
    return HttpResponse("<p>Crypto Currency rates updated!</p>"+str(updates))


def history(request):
    history_list = handler.get_price_history('inr', '', '')
    template = loader.get_template('history.html')
    context = Context({'requested_url': request.path_info, 'history_list': history_list})
    return HttpResponse(Template.render(template, context))


def auth_callback(request):
    access_token = request.GET['code'] if request.GET.__contains__('code') != '' else ''
    handler.store_auth_token(request)
    return HttpResponse("<p>auth callback received : "+access_token+"</p>")


def authorize(request):
    handler.request_access_token('unocoin')
    return HttpResponse("<p>Got access token!")


def refresh_token(request):
    return HttpResponse("<p>This is a refresh_token</p>")


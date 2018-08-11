import re
import shopify
from dbk_app.settings import API_KEY, API_SECRET_KEY, APP_URL
from shopify_app.models import DbkOrder
from django.shortcuts import render, redirect, reverse
from django.contrib import messages


def _return_address(request):
    return request.session.get('return_to') or reverse('home')


def home(request):
    """
    Fetch and return the 10 latest orders
    """
    orders = DbkOrder.objects.all()[:10]
    context = {"orders": orders}
    return render(request, "shopify_app/home.html", context)


def install(request):
    """install
    The view that is called when a user installs the app

    :param request:
    """
    shopify.Session.setup(api_key=API_KEY, secret=API_SECRET_KEY)
    session = shopify.Session("%s.myshopify.com" % (request.GET['shop']))
    scope = ['read_orders', 'write_orders', 'read_products']
    permission_url = session.create_permission_url(scope, 'https://%s/auth' % (APP_URL))
    return redirect(permission_url)


def auth(request):
    """auth
    The view that finally authenticates the user

    :param request:
    """
    shop = request.GET['shop']
    # hmac = request.GET['hmac']
    print("Well, I got this far!")

    if ".myshopify.com" in shop and re.match("^[A-Za-z0-9_-]*$", shop):
        session = shopify.Session(shop)
        request.session['shopify'] = {
            'shop_url': shop,
            'access_token': session.request_token(request.REQUEST),
        }

    messages.info(request, "Logged in to shopify store")
    response = redirect(_return_address(request))
    request.session.pop('return_to', None)
    return response

# Create your views here.

from django.shortcuts import render_to_response
from mysite.plainbrag.models import User, Product, UserProduct
from mysite.plainbrag.forms import ProductForm
import datetime
from django import http
import conf
from fbapi import Facebook
from django.utils import simplejson as json
from uuid import uuid4
from random import randrange
import cgi
from django.core import serializers
import time
import sets
import logging

logger = logging.getLogger(__name__)

_USER_FIELDS = u'name,email,picture,friends'
csrf_protect = True

def htmlescape(text):
    """Escape text for use as HTML"""
    return cgi.escape(
        text, True).replace("'", '&#39;').encode('ascii', 'xmlcharrefreplace')

def home(request):
    user, user_cookie, friendslist = init_facebook(request)
    products=None
    latest_products = UserProduct.objects.all()
    titlelist =[userproduct.product.title for userproduct in latest_products]
    set = sets.Set(titlelist)
    titlelist= list(set)
    titlestr =','.join([title for title in titlelist])
    print 'title str',titlestr
    prod_str=''

    js_conf = json.dumps({
	u'appId': conf.FACEBOOK_APP_ID,
	u'canvasName': conf.FACEBOOK_CANVAS_NAME,
	u'userIdOnServer': user.user_id if user else None,
    })
 
    if user:
        print 'there is a user in fb session'
        target='mypage.html'
	theuser = User.objects.get(user_id=user.user_id)
	products = theuser.userproduct_set.all()
	prod_str = get_products_list(user.user_id);

    else:
        target='welcome.html'
        print 'there is no user yet... '

    response = render_to_response(target,{'js_conf':js_conf,
	    'app_name':conf.APP_NAME, 'logged_in_user':user,'friends':friendslist,
	    'products':products,'latest_products':latest_products,'titlestr':titlestr,
	    'prodjson':prod_str});

    if not 'c' in request.COOKIES:
	csrf_token = str(uuid4())[:8]
	response.set_cookie("c",csrf_token)
    #print request
    #if request.method == u'POST' and csrf_protect and \
#	    csrf_token != request.POST.get(u'_csrf_token'):
#	raise CsrfException(u'Missing or invalid CSRF token.')

#print request.COOKIES

    response.set_cookie("u",user_cookie,None,datetime.timedelta(minutes=1440))
    return response

def add_product(request):
    title_p=''
    link_p=''
    userid_p=''
    image_link_p=''
    description_p=''
    _csrf_token_p=''
    if request.method == 'POST':
	if '_csrf_token' in request.POST:
	    _csrf_token_p = request.POST['_csrf_token'].strip()
	if 'user_id' in request.POST:
	    userid_p = request.POST['user_id'].strip()
	if 'title' in request.POST:
	    title_p = request.POST['title'].strip()
	if 'link' in request.POST:
	    link_p = request.POST['link'].strip()
	if 'image_link' in request.POST:
	    image_link_p = request.POST['image_link'].strip()
	if 'description' in request.POST:
	    description_p = request.POST['description'].strip()
	if 'price' in request.POST:
	    price_p = request.POST['price'].strip()
	
	date = None
	try:
	    date_year = int(request.POST[u'date_year'].strip())
	    date_month = int(request.POST[u'date_month'].strip())
	    date_day = int(request.POST[u'date_day'].strip())
	    if date_year < 0 or date_month < 0 or date_day < 0:
		raise RunException(u'Invalid date.')
	    date = datetime.date(date_year, date_month, date_day)
        except ValueError:
	    pass

	product_p = Product.objects.create(id=None, 
		title=title_p,
		link=link_p,
		image_link=image_link_p,
		description=description_p,
		)
	user_p = User.objects.get(user_id=userid_p)
	user_product = UserProduct(user=user_p, product = product_p, purchase_date=date, price=price_p)
	print 'printing product'
        print product_p
	user_product.save()
        if request.is_ajax():
            data = get_products_list(userid_p);
	    content_type = 'application/json'
	    return http.HttpResponse(data,content_type)

	return http.HttpResponseRedirect('/mypageproxy/%s/' % userid_p)

def list_titles(request):
    latest_products = UserProduct.objects.all()
    titlelist =[userproduct.product.title for userproduct in latest_products]
    data = json.dumps({
	u'titles': titlelist,
    })
    content_type = 'application/json'
    return http.HttpResponse(data,content_type)

def view_products(request,userid):
    try:
        user_id=int(userid)
    except ValueError:
	raise Http404()


    user = User.objects.get(user_id=user_id)
    #products = user.product_set.all()
    products = user.userproduct_set.all()
    latest_products = UserProduct.objects.all()
    js_conf = json.dumps({
	u'appId': conf.FACEBOOK_APP_ID,
	u'canvasName': conf.FACEBOOK_CANVAS_NAME,
	u'userIdOnServer': user.user_id if user else None,
    })
    target='mypage.html'
    response = render_to_response(target,{'js_conf':js_conf,
	    'app_name':conf.APP_NAME, 'logged_in_user':user,'products':products, 
	    'latest_products':latest_products});
    return response


def init_csrf(request):
    """Issue and handle CSRF token as necessary"""
    csrf_token = request.cookies.get(u'c')
    if not csrf_token:
	csrf_token = str(uuid4())[:8]
	set_cookie('c', csrf_token)
    if request.method == u'POST' and csrf_protect and \
	    csrf_token != request.POST.get(u'_csrf_token'):
	raise CsrfException(u'Missing or invalid CSRF token.')

def init_facebook(request):
    """Sets up the request specific Facebook and User instance"""
    facebook = Facebook()
    user = None
    friendslist = {}
    randomfriends = {}

    if u'signed_request' in request.POST:
        print 'POST request from FB with signed_request'
	facebook.load_signed_request(request.POST['signed_request'])
	#request.META['REQUEST_METHOD'] = u'GET'
    elif 'u' in request.COOKIES:
	facebook.load_signed_request(request.COOKIES['u'])

    # try to load or create a user object
    # load from db and update access_token
    if facebook.user_id:
        try:
	    user = User.objects.get(user_id=facebook.user_id)
        except User.DoesNotExist:
	    pass
        if user:
	    print 'User found in db'
	    if facebook.access_token and \
		    facebook.access_token != user.access_token:
		user.access_token = facebook.access_token
	    user.save()
	    if not facebook.access_token:
		facebook.access_token = user.access_token
#	    if user.dirty:
#	        user.refresh_data()
	    #get friendslist 
	    try:
# me = {}
		me = facebook.api(u'/me', {u'fields': _USER_FIELDS})
		friends = [auser for auser in me[u'friends'][u'data']]
		i=0
		for friend in friends:
                    uid=friend[u'id']
                    fn=friend[u'name']
		    frn = User(user_id=uid, first_name=fn)
		    friendslist[i]=frn
		    i=i+1
		randomfriends = select_random(friendslist, 10)
	    except KeyError, ex:
		pass # ignore if can't get the minimum fields

            print 'printing user = ',user


	if not user and facebook.access_token:
	    me = facebook.api(u'/me', {u'fields': _USER_FIELDS})
	    try:
	        # this should be a list of friends using this app
		friends = [auser for auser in me[u'friends'][u'data']]
		friendsstr =','.join([user[u'id'] for user in me[u'friends'][u'data']])
		i=0
		for friend in friends:
                    uid=friend[u'id']
                    fn=friend[u'name']
		    frn = User(user_id=uid, first_name=fn)
		    friendslist[i]=frn
		    i=i+1
		randomfriends = select_random(friendslist, 10)
                thename = me[u'name']
		namelist = thename.split(' ')
		fname=''
		lname =''
		if (len(namelist)) > 1: 
		    fname = namelist[0]
		    lname = namelist[1]
		else:
		    fname = thename

		print 'first name ',fname
		print 'last name ',lname
		user = User(
		    user_id=facebook.user_id, friends=friendsstr, 
		    access_token=facebook.access_token, name=me[u'name'],
		    first_name = fname, last_name = lname,
		    email=me.get(u'email'), picture=me[u'picture'])
		user.save()

	    except KeyError, ex:
		pass # ignore if can't get the minimum fields
    else:
        print 'No user id in fb'


    return user,facebook.user_cookie,randomfriends

def get_products_list(userid):
    user_p = User.objects.get(user_id=userid)
    products = user_p.userproduct_set.all()
    product_list = []
    for p in products:
	json_str = json.dumps(htmlescape(p.product.title)) 
	p.publish_title = json_str
    for uproduct in products:
	uprd = {}
	uprd['title']= uproduct.product.title
	uprd['price']= uproduct.price
	uprd['date']= uproduct.purchase_date.strftime('%h. %d, %Y')
	uprd['publish_title']= uproduct.publish_title
	print 'will print time now'
	test_time = uproduct.purchase_date.strftime('%h. %d, %Y')
	print 'test_time ',test_time
	product_list.append(uprd)
    data = 'test 2'
    print 'product_list ',product_list
    data = json.dumps(product_list)
    return data


def select_random(coll, limit):
    """Select a limited set of random non Falsy values from a list"""
    final = {}
    size = len(coll)
    i=0
    while limit and size:
        index = randrange(min(limit, size))
        size = size - 1
        elem = coll[index]
        coll[index] = coll[size]
        if elem:
            limit = limit - 1
            final[i]=elem
	    i = i+1
    return final
#


 


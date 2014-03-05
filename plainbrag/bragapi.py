import fbapi

class Bragapi(object):
    def init_facebook(request):
	facebook = Facebook()
	user = None

	if u'signed_request' in request.POST:
	    facebook.load_signed_request(request.get('signed_request'))
	    request.method = u'GET'
	    set_cookie(
		'u', facebook.user_cookie, datetime.timedelta(minutes=1440))
	elif 'u' in request.cookies:
	    facebook.load_signed_request(request.cookies.get('u'))

	if facebook.user_id:
	    if facebook.access_token:
		me = facebook.api(u'/me', {u'fields': _USER_FIELDS})
		try:
		    user = User(
			user_id=facebook.user_id, 
			access_token=facebook.access_token, first_name=me[u'name'],
			email=me.get(u'email'), picture=me[u'picture'])
		except KeyError, ex:
		    pass # ignore if can't get the minimum fields

	return user

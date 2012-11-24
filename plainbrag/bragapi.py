import fbapi

class Bragapi(object):
    def init_facebook(request):
	"""Sets up the request specific Facebook and User instance"""
	facebook = Facebook()
	user = None

	# initial facebook request comes in as a POST with a signed_request
	if u'signed_request' in request.POST:
	    facebook.load_signed_request(request.get('signed_request'))
	    # we reset the method to GET because a request from facebook with a
	    # signed_request uses POST for security reasons, despite it
	    # actually being a GET. in webapp causes loss of request.POST data.
	    request.method = u'GET'
	    set_cookie(
		'u', facebook.user_cookie, datetime.timedelta(minutes=1440))
	elif 'u' in request.cookies:
	    facebook.load_signed_request(request.cookies.get('u'))

	# try to load or create a user object
	if facebook.user_id:
#	user = User.get_by_key_name(facebook.user_id)
#if user:
		# update stored access_token
#	    if facebook.access_token and \
#		    facebook.access_token != user.access_token:
#		user.access_token = facebook.access_token
#		user.put()
#	    # refresh data if we failed in doing so after a realtime ping
#	    if user.dirty:
#		user.refresh_data()
		# restore stored access_token if necessary
#	    if not facebook.access_token:
#		facebook.access_token = user.access_token

#if not user and facebook.access_token:
	    if facebook.access_token:
		me = facebook.api(u'/me', {u'fields': _USER_FIELDS})
		try:
#friends = [user[u'id'] for user in me[u'friends'][u'data']]
		    user = User(
			user_id=facebook.user_id, 
			access_token=facebook.access_token, first_name=me[u'name'],
			email=me.get(u'email'), picture=me[u'picture'])
#user.put()
		except KeyError, ex:
		    pass # ignore if can't get the minimum fields

#    self.facebook = facebook
#    self.user = user
	return user

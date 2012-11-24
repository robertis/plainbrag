#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
from mysite.plainbrag.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^/$', home),
    (r'^home/$', home),
    (r'^addproduct/$', add_product) ,
    (r'^productTitles/$', list_titles) ,
    (r'^mypageproxy/(\d+)/$', view_products) ,
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

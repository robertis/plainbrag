from django.contrib import admin
from mysite.plainbrag.models import User, Product, Review, UserProduct

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(UserProduct)

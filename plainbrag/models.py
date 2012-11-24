from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    picture = models.CharField(max_length=100)
    email = models.EmailField(blank=True, verbose_name='e-mail')
    friends = models.TextField()
    dirty = models.BooleanField()

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __unicode__(self):
	return u'%s %s' % (self.first_name, self.last_name)

class Product(models.Model):
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='UserProduct')
    link = models.URLField()
    image_link = models.URLField()
    description = models.TextField()

    def __unicode__(self):
	return self.title

class Review(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbsup = models.IntegerField()
    thumbsdown = models.IntegerField()
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)

    def __unicode__(self):
	return self.title

class UserProduct(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    purchase_date = models.DateField()
    price = models.CharField(max_length=20)



# Create your models here.

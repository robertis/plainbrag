from django import forms
from mysite.plainbrag.models import Product,User

class ProductForm(forms.ModelForm):
    user = forms.ModelChoiceField(User.objects.all(), widget=forms.HiddenInput(), required=False)
    title = forms.CharField(max_length=100)
    link = forms.URLField(required=False)
    image_link = forms.URLField(required=False)
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
	model= Product




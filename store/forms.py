from django import forms
from django_countries.fields import CountryField
from .models import Review

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder':'1234 Main St.'}))
    apartment_address = forms.CharField(
        required=False, widget=forms.TextInput(
            attrs={'placeholder':'Apartment or suite'}))
    country = CountryField(blank_label='(select country)').formfield()
    zip = forms.CharField(required=False)
    same_shipping_address = forms.BooleanField(
        required=False,widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class ReviewForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your review',
        'id': 'usercomment',
        'rows': '4'
        }))
    class Meta:
        model = Review
        fields = ('content',)

    
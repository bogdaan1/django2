from django import forms
from .models import Order, Review, RATE_CHOICES
from .bulma_mixin import BulmaMixin

class OrderForm(BulmaMixin, forms.ModelForm):
    address = forms.CharField(label = 'Write your adress')
    phone = forms.CharField(label='Write your phone')

    class Meta:
        model = Order
        fields = ['address', 'phone']

class RateForm(BulmaMixin, forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea'}),
        label='Leave yor review here...')
    rate = forms.ChoiceField(
        choices=RATE_CHOICES,
        required=True,
        label='Rate product form 1 to 5'
    )

    class Meta:
        model = Review
        fields = ['text', 'rate']
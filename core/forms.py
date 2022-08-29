from django import forms
from .models import PaymentItem

class PaymentItemForm(forms.ModelForm):
    class Meta:
        model = PaymentItem
        fields = [
            'product', 'count'
        ]
    
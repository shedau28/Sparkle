from django import forms

class PaymentFrom(forms.Form):
    Name = forms.CharField(max_length=10)
    Amount = forms.IntegerField(max_value=10)
    Submit = forms.CharField( widget=forms.TextInput(attrs={'type': 'submit'}))
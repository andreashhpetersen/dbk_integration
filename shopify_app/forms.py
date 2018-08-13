from django import forms

class ImportOrdersForm(forms.Form):
    number_of_orders = forms.IntegerField()

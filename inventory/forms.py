from django import forms
from .models import Product,ProductReturn
from pos.models import Sell


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'color', 'size', 'quantity', 'price','discount','image', 'productioncost', 'transportcost', 'additionalcost']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control','min':'1'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'productioncost': forms.NumberInput(attrs={'class': 'form-control'}),
            'transportcost': forms.NumberInput(attrs={'class': 'form-control'}),
            'additionalcost': forms.NumberInput(attrs={'class': 'form-control'}),
        }
     


class ProductReturnForm(forms.ModelForm):
    class Meta:
        model = ProductReturn
        fields = ('product', 'quantity')
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control','min':'1'}),
        }
        
     


class SellUpdateForm(forms.ModelForm):
    class Meta:
        model = Sell
        fields = ['order','customer', 'phone', 'paymentstatus', 'address','status']     
        widgets = {
            'order': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'paymentstatus': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(),
        }
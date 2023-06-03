from django import forms
from .models import Category, Product,ProductReturn

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'color', 'size', 'quantity', 'image', 'productioncost', 'transportcost', 'additionalcost']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
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
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
from django import forms
from .models import Item

# SENIOR PATTERN: ModelForm
# Instead of redefining every field (name = forms.CharField...), 
# we tell Django: "Look at the Item model and copy it."
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # We specify exactly which fields the user can fill out.
        # SECURITY: Never use '__all__'. It allows hackers to mess with internal fields.
        fields = ['category', 'name', 'price', 'quantity']
        
        # We can style the widgets here (like adding CSS classes)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
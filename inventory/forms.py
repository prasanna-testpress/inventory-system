from django import forms
from .models import Item,Review

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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        
        # UI Polish: Make the comment box smaller so it doesn't take up the whole page
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your review...'}),
        }
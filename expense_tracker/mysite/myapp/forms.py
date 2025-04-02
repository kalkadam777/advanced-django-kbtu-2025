from django.forms import ModelForm
from django import forms
from .models import Expense, Category, GroupExpense

class ExpenseForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
class GroupExpenseForm(forms.ModelForm):
    class Meta:
        model = GroupExpense
        fields = ['name', 'total_amount', 'category', 'date', 'participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
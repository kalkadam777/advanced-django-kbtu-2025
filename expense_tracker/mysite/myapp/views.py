import datetime
from django.shortcuts import render, redirect
from .forms import ExpenseForm, CategoryForm, GroupExpenseForm
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, Category, GroupExpense
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

def group_expense_list(request):
    group_expenses = GroupExpense.objects.all()
    if request.method == 'POST':
        form = GroupExpenseForm(request.POST)
        if form.is_valid():
            group_expense = form.save()
            return redirect('group_expense_list')
    else:
        form = GroupExpenseForm()
    return render(request, "myapp/group_expense_list.html", {
        "group_expenses": group_expenses,
        "form": form,
    })
    


def expense_list(request):
    categories = Category.objects.all()
    category_filter = request.GET.get('category')
    date_filter = request.GET.get('date')
    expenses = Expense.objects.all()
    if category_filter:
        expenses = expenses.filter(category__id=category_filter)
    if date_filter:
        expenses = expenses.filter(date=date_filter)
    return render(request, 'myapp/expense_list.html', {
        'expenses': expenses,
        'categories': categories,
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CategoryForm()
    return render(request, 'myapp/add_category.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = UserCreationForm()
        return render(request, 'myapp/register.html', {'form': form})
        

def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
    
    expenses = Expense.objects.filter(user=request.user)
    total_expenses = expenses.aggregate(Sum('amount'))
    
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))
    
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))
    
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    
    expense_form = ExpenseForm()
    return render(request, 'myapp/index.html', {'expense_form':expense_form, 
                                                'expenses':expenses, 
                                                'total_expenses':total_expenses, 
                                                'yearly_sum':yearly_sum, 
                                                'monthly_sum': monthly_sum, 
                                                'weekly_sum':weekly_sum, 
                                                'daily_sums':daily_sums, 
                                                'categorical_sums':categorical_sums})

def edit(request, id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    
    if request.method == 'POST':
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    
    return render(request, 'myapp/edit.html', {'expense_form': expense_form})

def delete(request, id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
    
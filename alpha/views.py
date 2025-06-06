from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm, ExpenseForm
from .models import Income, Expense

def home(request):
    return render(request, 'tracker/home.html')

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'tracker/add_income.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

@login_required
def income_list(request):
    income = Income.objects.filter(user=request.user)
    return render(request, 'tracker/income_list.html', {'income': income})

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'tracker/expense_list.html', {'expenses': expenses})

@login_required
def dashboard(request):
    user = request.user

    total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    recent_income = Income.objects.filter(user=user).order_by('-date')[:5]
    recent_expenses = Expense.objects.filter(user=user).order_by('-date')[:5]

    recent_transactions = sorted(
        list(recent_income) + list(recent_expenses),
        key=lambda x: x.date,
        reverse=True
    )[:10]

    monthly_data = {}

    for income in Income.objects.filter(user=user):
        month = income.date.strftime('%B')
        monthly_data.setdefault(month, 0)
        monthly_data[month] += income.amount

    for expense in Expense.objects.filter(user=user):
        month = expense.date.strftime('%B')
        monthly_data.setdefault(month, 0)
        monthly_data[month] -= expense.amount

    months = list(monthly_data.keys())
    totals = list(monthly_data.values())

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'recent_transactions': recent_transactions,
        'months': months,
        'totals': totals,
    }

    return render(request, 'tracker/dashboard.html', context)

@login_required
def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'tracker/edit_income.html', {'form': form})

@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'tracker/delete_income.html', {'income': income})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after signup
            return redirect('dashboard')  # Or your app’s home page
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})



from django.shortcuts import render,redirect
from ManageCaahApp.models import *
from ManageCaahApp.forms import *
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


def register_page(request):
    if request.method == 'POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Registration Successfull')
            return redirect('login_page')
        
    else:
        form_data = RegistrationForm()
    context = {
        'form_data' : form_data,
        'form_name' : 'Registration Form',
        'form_btn' : 'Register'
    }

    return render(request, 'master/base-form.html', context)

def login_page(request):
    if request.method == 'POST':
        form_data = LoginForm(request, data= request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Login Successfull')
                return redirect('dashboard')
    else:
        form_data = LoginForm()
    context = {
        'form_data' : form_data,
        'form_name' : 'Login Form',
        'form_btn' : 'Login'
    }

    return render(request, 'master/base-form.html', context)
@login_required
def dashboard(request):
    cash_data = AddCash.objects.filter(user=request.user)
    expense_data = ExpenseModel.objects.filter(user=request.user)

    total_income = cash_data.aggregate(
        total =Sum('amount')
    )['total'] or 0

    total_expense = expense_data.aggregate(
        total=Sum('amount')
    )['total'] or 0

    current_balance = total_income-total_expense

    context={
        'total_income': total_income,
        'total_expense' : total_expense,
        'current_balance' : current_balance,
        'expense_data' : expense_data,
        'cash_data' : cash_data
    }

    return render(request, 'dashboard.html' , context)

@login_required
def logout_page(request):
    logout(request)
    messages.success(request, 'Logout Successfull')
    return redirect('login_page')

@login_required
def profile_update(request):
    try:
        current_user = request.user
    except:
        current_user = None

    if request.method == 'POST':
        form_data = UserModifyForm(request.POST, instance = current_user)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Profile Update Successfull')
            return redirect('dashboard')
        
    else:
        form_data = UserModifyForm(instance = current_user)
    context = {
        'form_data' : form_data,
        'form_name' : 'Profile Update Form',
        'form_btn' : 'Profile Update'
    }

    return render(request, 'master/base-form.html' , context)

def cash_list(request):
    cash_data = AddCash.objects.filter(user= request.user)

    context={
        'cash_data' : cash_data,
    }

    return render(request, 'cash-list.html', context)

def add_cash(request):
    if request.method == 'POST':
        form_data = AddCashForm(request.POST)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Successfull')
            return redirect('cash_list')
        
    else:
        form_data = AddCashForm()
    context = {
        'form_data' : form_data,
        'form_name' : 'Add Cash Form',
        'form_btn' : 'Add Cash'
    }

    return render(request, 'master/base-form.html', context)

@login_required
def update_cash(request, id):
    cash_data = AddCash.objects.get(id=id)
    if request.method == 'POST':
        form_data = AddCashForm(request.POST, instance=cash_data)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Successfull')
            return redirect('cash_list')
        
    else:
        form_data = AddCashForm(instance=cash_data)
    context = {
        'form_data' : form_data,
        'form_name' : 'Update Cash Form',
        'form_btn' : 'Update Cash'
    }

    return render(request, 'master/base-form.html', context)

@login_required
def delete_cash(request,id):
    cash_data = AddCash.objects.get(id=id)
    cash_data.delete()
    return redirect('cash_list')

@login_required
def expense_list(request):
    expense_data = ExpenseModel.objects.filter(user= request.user)

    context={
        'expense_data' : expense_data,
    }

    return render(request, 'expense-list.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form_data = ExpenseForm(request.POST)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Successfull')
            return redirect('expense_list')
        
    else:
        form_data = ExpenseForm()
    context = {
        'form_data' : form_data,
        'form_name' : 'Add Expense Form',
        'form_btn' : 'Add Expense'
    }

    return render(request, 'master/base-form.html', context)

@login_required
def update_expense(request, id):
    expense_data = ExpenseModel.objects.get(id=id)
    if request.method == 'POST':
        form_data = ExpenseForm(request.POST, instance=expense_data)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Successfull')
            return redirect('cash_list')
        
    else:
        form_data = AddCashForm(instance=expense_data)
    context = {
        'form_data' : form_data,
        'form_name' : 'Update Expense Form',
        'form_btn' : 'Update Expense'
    }

    return render(request, 'master/base-form.html', context)

@login_required
def delete_expense(request,id):
  expense_data=ExpenseModel.objects.get(id=id)
  expense_data.delete()
  return redirect('expense_list')
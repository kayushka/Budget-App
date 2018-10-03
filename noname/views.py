from audioop import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views import View
from noname.forms import AddIncomeForm, AddExpensesForm, UserCreationForm2
from noname.models import Income, Expenses


class Home(View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        all_income = Income.objects.filter(user=user, created_at__month=current_month)
        all_expenses = Expenses.objects.filter(user=user, created_at__month=current_month)
        return render(request, 'noname/home.html')
    # todo balans dla danego miesiąca (wszystkie incomy minus wszystkie wydatki)
    # todo linki do każdej kategorii wydatków danego miesiąca
    # todo w każdym linku u gory podsumowanie wydatków
    # todo w każdym linku podsumowanie wydatków w każdej podkategorii


class List(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        all_income = Income.objects.filter(user=user).order_by('date')
        all_expenses = Expenses.objects.filter(user=user).order_by('date')
        ctx = {
            "allIncome": all_income,
            "allExpenses": all_expenses
        }
        return render(request, 'noname/list.html', ctx)


class AddIncome(LoginRequiredMixin, View):
    def get(self, request):
        form = AddIncomeForm()
        return render(request, 'noname/add_income.html', {'form': form})

    def post(self, request):
        form = AddIncomeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            category = form.cleaned_data['category']
            income = Income.objects.create(amount=amount, category=category)
            return redirect('list')
        else:
            return render(request, 'noname/add_income.html', {'form': form})


class AddExpense(View):
    def get(self, request):
        form = AddExpensesForm()
        return render(request, 'noname/add_expense.html', {'form': form})

    def post(self, request):
        form = AddExpensesForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            category = form.cleaned_data['category']
            expense = Expenses.objects.create(amount=amount, category=category)
            return redirect('list')
        else:
            return render(request, 'noname/add_expense.html', {'form': form})


class SignUp(View):
    def get(self, request):
        form = UserCreationForm2()
        return render(request, 'noname/add_user.html', {'form': form})

    def post(self, request):
        form = UserCreationForm2(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get['username']
            raw_password = form.cleaned_data.get['password1']
            user = authenticate(request, username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            form = UserCreationForm()
            return render(request, 'noname/add_user.html', {'form': form})

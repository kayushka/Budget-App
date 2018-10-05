from django.shortcuts import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.core.serializers import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views import View
from noname.forms import AddIncomeForm, AddExpensesForm, UserCreationForm2
from noname.models import Income, Expenses


class Main(View):
    def get(self, request):
        return render(request, 'noname/main.html')


class DeleteExpense(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user
        object = Expenses.objects.get(user=user, id=id)
        object.delete()
        return redirect(reverse("list"))


class DeleteIncome(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user
        object = Income.objects.get(user=user, id=id)
        object.delete()
        return redirect(reverse("list"))


class EditExpense(View):
    def post(self, request, id):
        user = request.user
        object = Expenses.objects.get(user=user, id=id)


class Json(View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        foods = Expenses.objects.filter(user=user, date__month=current_month, category__range=(1, 4))
        food = 0.0
        for f in foods:
            food += f.amount
        houses = Expenses.objects.filter(user=user, date__month=current_month, category__range=(5, 13))
        house = 0.0
        for h in houses:
            house += h.amount
        transports = Expenses.objects.filter(user=user, date__month=current_month, category__range=(14, 19))
        transport = 0.0
        for t in transports:
            transport += t.amount
        communications = Expenses.objects.filter(user=user, date__month=current_month, category__range=(20, 22))
        communication = 0.0
        for c in communications:
            communication += c.amount
        healths = Expenses.objects.filter(user=user, date__month=current_month, category__range=(23, 25))
        health = 0.0
        for q in healths:
            health += q.amount
        clothes = Expenses.objects.filter(user=user, date__month=current_month, category__range=(26, 27))
        cloth = 0.0
        for cl in clothes:
            cloth += cl.amount
        cosmetics = Expenses.objects.filter(user=user, date__month=current_month, category__range=(28, 30))
        cosmetic = 0.0
        for cc in cosmetics:
            cosmetic += cc.amount
        children = Expenses.objects.filter(user=user, date__month=current_month, category__range=(31, 35))
        child = 0.0
        for ch in children:
            child += ch.amount
        entertainments = Expenses.objects.filter(user=user, date__month=current_month, category__range=(36, 39))
        entertainment = 0.0
        for e in entertainments:
            entertainment += e.amount
        others = Expenses.objects.filter(user=user, date__month=current_month, category__range=(40, 46))
        other = 0.0
        for o in others:
            other += o.amount
        all = [
            ["task", 'house per day'],
            ["jedzenie", food],
            ["dom", house],
            ["tranport", transport],
            ["komunikacja", communication],
            ["zdrowie", health],
            ["ubrania", cloth],
            ["kosmetyki", cosmetic],
            ["dzieci", child],
            ["rozrywka", entertainment],
            ["inne", other]
        ]
        return JsonResponse(all, safe=False)


class Home(LoginRequiredMixin, View):
    def get(self, request):
        mnth = ['STYCZEŃ', 'LUTY', 'MARZEC', 'KWIECIEŃ', 'MAJ', 'CZERWIEC', 'LIPIEC', 'SIERPIEŃ',
                'WRZESIEŃ', 'PAŹDZIERNIK', 'LISTOPAD', 'GRUDZIEŃ']
        current_month = datetime.now().month
        user = request.user
        incomes = Income.objects.filter(user=user, date__month=current_month)
        income = 0.0
        for i in incomes:
            income += float(i.amount)
        expenses = Expenses.objects.filter(user=user, date__month=current_month)
        expense = 0.0
        for e in expenses:
            expense += float(e.amount)
        sum = float(income) - float(expense)
        if income != 0.0:
            a = (expense / income) * 100
        else:
            a = 0.0
        last = Expenses.objects.filter(user=user).order_by('-date')[:5]
        ctx = {
            "last": last,
            "a": a,
            "month": mnth[int(current_month) - 1],
            "income": income,
            "expense": expense,
            "sum": sum
        }
        return render(request, 'noname/home.html', ctx)


class List(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        mnth = ['STYCZEŃ', 'LUTY', 'MARZEC', 'KWIECIEŃ', 'MAJ', 'CZERWIEC', 'LIPIEC', 'SIERPIEŃ',
                'WRZESIEŃ', 'PAŹDZIERNIK', 'LISTOPAD', 'GRUDZIEŃ']
        current_month = datetime.now().month
        incomes = Income.objects.filter(user=user, date__month=current_month)
        income = 0.0
        for i in incomes:
            income += float(i.amount)
        expenses = Expenses.objects.filter(user=user, date__month=current_month)
        expense = 0.0
        for e in expenses:
            expense += float(e.amount)
        all_income = Income.objects.filter(user=user).order_by('-date')
        all_expenses = Expenses.objects.filter(user=user).order_by('-date')
        ctx = {
            "month": mnth[int(current_month) - 1],
            "income": income,
            "expense": expense,
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
            comment = form.cleaned_data['comment']
            user = request.user
            income = Income.objects.create(amount=amount, category=category, user=user, comment=comment)
            return redirect('list')
        else:
            return render(request, 'noname/add_income.html', {'form': form})


class AddExpense(LoginRequiredMixin, View):
    def get(self, request):
        form = AddExpensesForm()
        return render(request, 'noname/add_expense.html', {'form': form})

    def post(self, request):
        form = AddExpensesForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            category = form.cleaned_data['category']
            comment = form.cleaned_data['comment']
            user = request.user
            expense = Expenses.objects.create(amount=amount, category=category, user=user, comment=comment)
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
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            form = UserCreationForm()
            return render(request, 'noname/add_user.html', {'form': form})


class Incomes(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        incomes = Income.objects.filter(user=user, date__month=current_month, category__range=(1, 5))
        income = 0.0
        for i in incomes:
            income += float(i.amount)
        Salary = Income.objects.filter(user=user, date__month=current_month, category=1)
        salary = 0.0
        for s in Salary:
            salary += float(s.amount)
        Salary2 = Income.objects.filter(user=user, date__month=current_month, category=2)
        salary2 = 0.0
        for ss in Salary2:
            salary2 += float(ss.amount)
        Bonus = Income.objects.filter(user=user, date__month=current_month, category=3)
        bonus = 0.0
        for b in Bonus:
            bonus += float(b.amount)
        Sale = Income.objects.filter(user=user, date__month=current_month, category=4)
        sale = 0.0
        for sss in Sale:
            sale += float(sss.amount)
        Other = Income.objects.filter(user=user, date__month=current_month, category=5)
        other = 0.0
        for o in Other:
            other += float(o.amount)
        ctx = {
            "income": income,
            "salary": salary,
            "salary2": salary2,
            "bonus": bonus,
            "sale": sale,
            "other": other,
        }
        return render(request, 'noname/income.html', ctx)


class Food(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        iHouse = Expenses.objects.filter(user=user, date__month=current_month, category=1)
        house = 0.0
        for h in iHouse:
            house += float(h.amount)
        eatingOut = Expenses.objects.filter(user=user, date__month=current_month, category=2)
        eatingout = 0.0
        for e in eatingOut:
            eatingout += float(e.amount)
        Work = Expenses.objects.filter(user=user, date__month=current_month, category=3)
        work = 0.0
        for w in Work:
            work += float(w.amount)
        Alcohol = Expenses.objects.filter(user=user, date__month=current_month, category=4)
        alc = 0.0
        for a in Alcohol:
            alc += float(a.amount)
        summ = house + eatingout + work + alc
        ctx = {
            "sum": summ,
            "house": house,
            "eatingout": eatingout,
            "work": work,
            "alc": alc,
        }
        return render(request, 'noname/food.html', ctx)


class House(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        Rent = Expenses.objects.filter(user=user, date__month=current_month, category=1)
        rent = 0.0
        for r in Rent:
            rent += float(r.amount)
        Water = Expenses.objects.filter(user=user, date__month=current_month, category=2)
        water = 0.0
        for w in Water:
            water += float(w.amount)
        Energy = Expenses.objects.filter(user=user, date__month=current_month, category=3)
        energy = 0.0
        for e in Energy:
            energy += float(e.amount)
        Gas = Expenses.objects.filter(user=user, date__month=current_month, category=4)
        gas = 0.0
        for g in Gas:
            gas += float(g.amount)
        Heating = Expenses.objects.filter(user=user, date__month=current_month, category=5)
        heat = 0.0
        for h in Heating:
            heat += float(h.amount)
        Garbage = Expenses.objects.filter(user=user, date__month=current_month, category=6)
        garb = 0.0
        for _ in Garbage:
            garb += float(_.amount)
        Repair = Expenses.objects.filter(user=user, date__month=current_month, category=7)
        repair = 0.0
        for r in Repair:
            repair += float(r.amount)
        Equipment = Expenses.objects.filter(user=user, date__month=current_month, category=8)
        equip = 0.0
        for q in Equipment:
            equip += float(q.amount)
        Insurance = Expenses.objects.filter(user=user, date__month=current_month, category=9)
        insurance = 0.0
        for i in Insurance:
            insurance += float(i.amount)
        summ = insurance+equip+repair+garb+heat+gas+energy+water+rent
        ctx = {
            'sum': summ,
            'insurance': insurance,
            'equip': equip,
            'repair': repair,
            'garb': garb,
            'heat': heat,
            'gas': gas,
            'energy': energy,
            'water': water,
            'rent': rent
        }
        return render(request, 'noname/house.html', ctx)


class Transport(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        Gas = Expenses.objects.filter(user=user, date__month=current_month, category=14)
        gas = 0.0
        for g in Gas:
            gas += float(g.amount)
        Repair = Expenses.objects.filter(user=user, date__month=current_month, category=15)
        repair = 0.0
        for r in Repair:
            repair += float(r.amount)
        Equipment = Expenses.objects.filter(user=user, date__month=current_month, category=16)
        equip = 0.0
        for e in Equipment:
            equip += float(e.amount)
        Insurance = Expenses.objects.filter(user=user, date__month=current_month, category=17)
        insurance = 0.0
        for i in Insurance:
            insurance += float(i.amount)
        Tickets = Expenses.objects.filter(user=user, date__month=current_month, category=18)
        ticket = 0.0
        for t in Tickets:
            ticket += float(t.amount)
        Taxi = Expenses.objects.filter(user=user, date__month=current_month, category=19)
        taxi = 0.0
        for _ in Taxi:
            taxi += float(_.amount)
        summ = insurance + equip + repair + gas + taxi + ticket
        ctx = {
            'sum': summ,
            'insurance': insurance,
            'equip': equip,
            'repair': repair,
            'taxi': taxi,
            'ticket': ticket,
            'gas': gas,
        }
        return render(request, 'noname/transport.html', ctx)


class Communication(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        Phone = Expenses.objects.filter(user=user, date__month=current_month, category=20)
        phone = 0.0
        for p in Phone:
            phone += float(p.amount)
        TV = Expenses.objects.filter(user=user, date__month=current_month, category=21)
        tv = 0.0
        for t in TV:
            tv += float(t.amount)
        Internet = Expenses.objects.filter(user=user, date__month=current_month, category=22)
        internet = 0.0
        for _ in Internet:
            internet += float(_.amount)
        summ = phone + tv + internet
        ctx = {
            'sum': summ,
            'phone': phone,
            'tv': tv,
            'internet': internet
        }
        return render(request, 'noname/communication.html', ctx)


class Health(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        Doctor = Expenses.objects.filter(user=user, date__month=current_month, category=23)
        doc = 0.0
        for p in Doctor:
            doc += float(p.amount)
        Medical = Expenses.objects.filter(user=user, date__month=current_month, category=24)
        medical = 0.0
        for t in Medical:
            medical += float(t.amount)
        Medicine = Expenses.objects.filter(user=user, date__month=current_month, category=25)
        medicine = 0.0
        for _ in Medicine:
            medicine += float(_.amount)
        summ = doc + medical + medicine
        ctx = {
            'sum': summ,
            'doc': doc,
            'medical': medical,
            'medicine': medicine
        }
        return render(request, 'noname/health.html', ctx)


class Clothes(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        Clothes = Expenses.objects.filter(user=user, date__month=current_month, category=26)
        clothes = 0.0
        for g in Clothes:
            clothes += float(g.amount)
        Shoes = Expenses.objects.filter(user=user, date__month=current_month, category=27)
        shoes = 0.0
        for r in Shoes:
            shoes += float(r.amount)
        summ = shoes + clothes
        ctx = {
            'sum': summ,
            'clothes': clothes,
            'shoes': shoes
        }
        return render(request, 'noname/clothes.html', ctx)


class Beauty(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        Cosmetic = Expenses.objects.filter(user=user, date__month=current_month, category=28)
        cosmetic = 0.0
        for p in Cosmetic:
            cosmetic += float(p.amount)
        Clean = Expenses.objects.filter(user=user, date__month=current_month, category=29)
        clean = 0.0
        for t in Clean:
            clean += float(t.amount)
        Hair = Expenses.objects.filter(user=user, date__month=current_month, category=30)
        hair = 0.0
        for _ in Hair:
            hair += float(_.amount)
        summ = hair + clean + cosmetic
        ctx = {
            'sum': summ,
            'cosmetic': cosmetic,
            'clean': clean,
            'hair': hair
        }
        return render(request, 'noname/beauty.html', ctx)


class Child(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        Things = Expenses.objects.filter(user=user, date__month=current_month, category=31)
        things = 0.0
        for g in Things:
            things += float(g.amount)
        Extras = Expenses.objects.filter(user=user, date__month=current_month, category=32)
        extras = 0.0
        for r in Extras:
            extras += float(r.amount)
        School = Expenses.objects.filter(user=user, date__month=current_month, category=33)
        school = 0.0
        for s in School:
            school += float(s.amount)
        Games = Expenses.objects.filter(user=user, date__month=current_month, category=34)
        games = 0.0
        for _ in Games:
            games += float(_.amount)
        Nanny = Expenses.objects.filter(user=user, date__month=current_month, category=35)
        nanny = 0.0
        for i in Nanny:
            nanny += float(i.amount)
        summ = things + extras + school + games + nanny
        ctx = {
            'sum': summ,
            'things': things,
            'extras': extras,
            'school': school,
            'games': games,
            'nanny': nanny
        }
        return render(request, 'noname/child.html', ctx)


class Entertainment(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        Sport = Expenses.objects.filter(user=user, date__month=current_month, category=36)
        sport = 0.0
        for y in Sport:
            sport += float(y.amount)
        Cinema = Expenses.objects.filter(user=user, date__month=current_month, category=37)
        cinema = 0.0
        for p in Cinema:
            cinema += float(p.amount)
        Concert = Expenses.objects.filter(user=user, date__month=current_month, category=38)
        concert = 0.0
        for t in Concert:
            concert += float(t.amount)
        Book = Expenses.objects.filter(user=user, date__month=current_month, category=39)
        book = 0.0
        for _ in Book:
            book += float(_.amount)
        summ = sport + cinema + concert + book
        ctx = {
            'sum': summ,
            'sport': sport,
            'cinema': cinema,
            'concert': concert,
            'book': book
        }
        return render(request, 'noname/entertainment.html', ctx)


class Other(LoginRequiredMixin, View):
    def get(self, request):
        current_month = datetime.now().month
        user = request.user
        Gifts = Expenses.objects.filter(user=user, date__month=current_month, category=40)
        gifts = 0.0
        for g in Gifts:
            gifts += float(g.amount)
        Spare = Expenses.objects.filter(user=user, date__month=current_month, category=41)
        spare = 0.0
        for r in Spare:
            spare += float(r.amount)
        Hotel = Expenses.objects.filter(user=user, date__month=current_month, category=42)
        hotel = 0.0
        for s in Hotel:
            hotel += float(s.amount)
        Hobby = Expenses.objects.filter(user=user, date__month=current_month, category=43)
        hobby = 0.0
        for _ in Hobby:
            hobby += float(_.amount)
        Education = Expenses.objects.filter(user=user, date__month=current_month, category=44)
        education = 0.0
        for i in Education:
            education += float(i.amount)
        Programs = Expenses.objects.filter(user=user, date__month=current_month, category=45)
        programs = 0.0
        for p in Programs:
            programs += float(p.amount)
        Other = Expenses.objects.filter(user=user, date__month=current_month, category=46)
        other = 0.0
        for o in Other:
            other += float(o.amount)
        summ = gifts + spare + hotel + hobby + education + programs + other
        ctx = {
            'sum': summ,
            'gifts': gifts,
            'spare': spare,
            'hotel': hotel,
            'hobby': hobby,
            'education': education,
            'programs': programs,
            'other': other
        }
        return render(request, 'noname/other.html', ctx)

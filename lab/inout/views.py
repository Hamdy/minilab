from forms import InOutForm
from analysis.models import Analysis
import datetime
from django.shortcuts import render
from dateutil.relativedelta import relativedelta
from inout.models import Income, Expenses

def inout(request):
    total_income = 0.0
    total_expenses = 0.0
    incomes = []
    expenses = []

    if request.method == "GET":
        form = InOutForm()
    else:
        form = InOutForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data.get('type')
            
            if type == 'today':
                today = datetime.date.today()
                incomes = Income.objects.filter(date=today)
                expenses = Expenses.objects.filter(date=today)
                   
            elif type == 'yesterday':
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
                incomes = Income.objects.filter(date=yesterday)
                expenses = Expenses.objects.filter(date=yesterday)
                
            elif type == 'last_week':
                week_ago = datetime.date.today() - datetime.timedelta(days=7)
                incomes = Income.objects.filter(date__gte=week_ago)
                expenses = Expenses.objects.filter(date__gte=week_ago)
            
            elif type == 'last_month':
                month_ago = datetime.date.today() - relativedelta(months=+1)
                incomes = Income.objects.filter(date__gte=month_ago)
                expenses = Expenses.objects.filter(date__gte=month_ago)
            
            elif type == 'last_year':
                year_ago = datetime.date.today() - relativedelta(years=+1)
                incomes = Income.objects.filter(date__gte=year_ago)
                expenses = Expenses.objects.filter(date__gte=year_ago)
                
            else:
                start = form.cleaned_data.get('start')
                end = form.cleaned_data.get('end')
                
                incomes = Income.objects.filter(date__range=(start, end))
                expenses = Expenses.objects.filter(date__range=(start, end))
                
            for i in incomes:  
                total_income += i.income
            for e in expenses:
                total_expenses += e.expenses
            
    return render(request, 'inout.html', {'income':total_income, 'expenses':total_expenses, 'form':form})
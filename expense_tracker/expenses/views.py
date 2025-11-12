import base64
import csv
import io
from django.shortcuts import render
# from .forms import ExpenseListForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Expense
from django.shortcuts import get_object_or_404,redirect
import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
# Create your views here.
# def index(request):
#     return render(request,'index.html')
@login_required
def expense_list(request):
    month = request.GET.get('month')
    if month:
        expenses = Expense.objects.filter(user=request.user,date__month=month)
        
    else:
        expenses = Expense.objects.filter(user=request.user)
        
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return render(request,'index.html',{'expenses':expenses,'months':months,'selected_month':month})

@login_required
def addExpense(request):
        if request.method == 'POST':
            title = request.POST.get('title')
            category = request.POST.get('category')
            amount = request.POST.get('amount')
            date = request.POST.get('date')
            is_recurring = request.POST.get('is_recurring')
            if is_recurring=='on':
                is_recurring=True
            else:
                is_recurring=False
            Expense.objects.create(
                user = request.user,
                title=title,
                category=category,
                amount=amount,
                date=date,
                is_recurring = is_recurring            
            )
            return redirect('index')
        else:
            return render(request,'addExpense.html')
@login_required
def removeExpense(request,expenseId):
    expense = get_object_or_404(Expense,pk=expenseId)
    if request.method=='POST':
        expense.delete()
        return redirect('index')
    return render(request,'removeExpense.html',{'expense':expense})
@login_required
def editExpense(request,expenseId):
    expense=get_object_or_404(Expense,pk=expenseId)
    if request.method=='POST':
        expense.title = request.POST.get('title')
        expense.category = request.POST.get('category')
        expense.amount = request.POST.get('amount')
        expense.date = request.POST.get('date')
        is_recurring = request.POST.get('is_recurring')
        if is_recurring=='on':
            expense.is_recurring=True
        else:
            expense.is_recurring=False
        expense.save()
        return redirect('index')
    else:
        return render(request,'editExpense.html',{'expense':expense})            
@login_required       
def filterExpense(request,month):
    return redirect(f"/?month={month}")

@login_required
def download_expenses(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="expenses.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title','Category','Amount','Date','is_recurring'])
    
    expenses = Expense.objects.filter(user=request.user)
    for exp in expenses:
        writer.writerow([exp.title,exp.category,exp.amount,exp.date.strftime('%d-%m-%Y'),exp.is_recurring])
    
    return response
@login_required
def analyze_category(request,category):
    expenses = Expense.objects.filter(user=request.user,category__iexact=category)
    if not expenses.exists():
        return render (request,'analysis.html',{'error':'No expenses found in {category}'})
    
    df = pd.DataFrame(list(expenses.values('amount','date')))
    df['amount']=pd.to_numeric(df['amount'])
    df.dropna(subset=['amount'],inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['month']=df['date'].dt.month
    month_totals = df.groupby('month')['amount'].sum().reindex(range(1,13),fill_value=0)
    
    month_names=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if month_totals.sum()==0:
        return render(request,'analysis.html',{'error':f'no Numeric expense for {category}'})
    fig,ax=plt.subplots()
    # print(month_totals)
    month_totals.plot(kind='bar',ax=ax)
    ax.bar(month_names,month_totals,color='teal')
    ax.set_title(f'Expense Trend in {category} over the months')
    ax.set_xlabel('Months')
    ax.set_ylabel('Amount spent')
    def save_chart_to_base64(fig):
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        encoded = base64.b64encode(image_png).decode('utf-8')
        return f"data:image/png;base64,{encoded}"

    chart = save_chart_to_base64(fig)
    return render(request,'analysis.html',{'chart':chart,'category':category})
    
def registerUser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2=request.POST.get('password2')
        if not username or not email or not password1 or not password2:
            return render(request, 'registration/register.html', {'error': 'All fields are required'})
        if password1!=password2:
            return render(request,'registration/register.html',{'error':'Password do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request,'registration/register.html',{'error':'Username already exists'})
        
        user = User.objects.create_user(username=username,email=email,password=password1)
        user.save()
        return redirect('login') 
    return render(request,'registration/register.html')

def loginUser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        user = authenticate(request,username=username,password=password1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,'registration/login.html',{'error':'Invalid Credentials'})
    return render(request,'registration/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')
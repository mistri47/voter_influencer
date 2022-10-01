from django.shortcuts import render, redirect

# Create your views here.
from expenses.models import Expense


def list_items(request):

    expenses = Expense.objects.all()

    return render(
        request,
        'expenses/list.html',
        {'expenses': expenses}
    )

def details(request, id):
    pass

def add(request):
    if request.method == 'POST':
        vikaskhand = request.POST['vikaskhand']
        panchayat = request.POST['panchayat']
        village_name = request.POST['village_name']
        workd_details = request.POST['workd_details']
        amount = request.POST['amount']
        department = request.POST['department']
        financial_year = request.POST['financial_year']

        print(vikaskhand,panchayat,village_name,workd_details,amount,department,financial_year)
        expenses_add = Expense(vikaskhand = vikaskhand, panchayat = panchayat, village_name = village_name,  workd_details = workd_details, amount = amount , department = department, financial_year = financial_year)
        expenses_add.save()

        return redirect('list_expenses')
    
    return render(
        request,
        'expenses/add.html',
        {}
    )


def update(request, id):
    pass

def delete(request, id):            
    if request.method == "POST":
        data = Expense.objects.get(pk=id)
        data.delete()

    return redirect('list_expenses')


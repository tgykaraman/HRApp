from django.shortcuts import render,redirect
from .forms import AddNewEmployee
from django.urls import reverse 
from .models import employee



# Create your views here.

def manageemployee(request):
    return render(request,"base.html")


def AddEmployee(request):
    if request.POST:
        form = AddNewEmployee(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("AddEmployee")
    else:
        form = AddNewEmployee()
    
    employees = employee.objects.all()
    return render(request,"newemployee.html",{"form":form, "employees":employees})


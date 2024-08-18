from django.shortcuts import render,redirect


# Create your views here.

def AddEmployee(request):
    return render(request,'hr_app/base.html')
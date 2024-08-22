from django.shortcuts import render,redirect,get_object_or_404
from .forms import AddNewEmployee
from django.urls import reverse 
from .models import Employee
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse

# Create your views here.

def manageemployee(request):
    employees = Employee.objects.all()
    return render(request,"manageemployee.html",{"employees":employees})


def AddEmployee(request):
    if request.method == 'POST':
        form = AddNewEmployee(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect("hr_app:addemployee")
        else:
            print("Form is not valid:", form.errors)  # Form hatalarını loglayın
            messages.error(request, "Employee couldn't be added. Please check the errors.")
    else:
        form = AddNewEmployee()
    
    employees = Employee.objects.all()
    return render(request, "newemployee.html", {"form": form, "employees": employees})


def edit_employee(request,id):
    employee = get_object_or_404(Employee,id=id)
    if request.method == "POST":
        form = AddNewEmployee(request.POST, request.FILES,instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request,"Employee edited successfully!")
            employees = Employee.objects.all()
            return render(request,"manageemployee.html",{"employees":employees})
        else:
            messages.error(request,"Employee couldn't be edited. Please check the errors.")
    else:
       form = AddNewEmployee(instance=employee)
    return render(request,"editemployee.html",{"form":form})

def export_employees_to_excel(request):
    employees = Employee.objects.all().values()
    df = pd.DataFrame(employees)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
    df.to_excel(response, index=False)
    return response

def deleteemployee(request,id):
    employee = Employee.objects.get(pk=id)
    Employee.objects.filter(id=id).delete()
    return redirect("hr_app:manageemployee")
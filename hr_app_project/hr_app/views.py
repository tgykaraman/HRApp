from django.shortcuts import render,redirect,get_object_or_404
from .forms import AddNewEmployee, AddNewJob, AddNewCandidate
from django.urls import reverse 
from .models import Employee, Recruitment, Candidate
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

def tablefilter(request):
    employees = Employee.objects.all()
    name_filter = request.GET.get("name")
    department_filter = request.GET.get("department")

    if name_filter:
        employees = employees.filter(name__icontains=name_filter).all()
    if department_filter:
        employees = employees.filter(department__icontains=department_filter).all()
    
    context = {"employees":employees,
               "name_filter": name_filter,
               "department_filter": department_filter}
    print(f"{name_filter} & {department_filter}")
    return render(request,"manageemployee.html",context=context)

def AddJob(request):
    if request.method == 'POST':
        form = AddNewJob(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, "Job added successfully!")
            return redirect("hr_app:addjob")
        else:
            print("Form is not valid:", form.errors)  # Form hatalarını loglayın
            messages.error(request, "Job couldn't be added. Please check the errors.")
    else:
        form = AddNewJob()
    
    jobs = Recruitment.objects.all()
    return render(request, "newjob.html", {"form": form, "jobs": jobs})

def AddCandidate(request):
    if request.method == 'POST':
        form_candidate = AddNewCandidate(request.POST, request.FILES)
        if form_candidate.is_valid():
            print("Form is valid")
            form_candidate.save()
            messages.success(request, "Candidate added successfully!")
            return redirect("hr_app:addcandidate")
        else:
            print("Form is not valid:", form_candidate.errors)  # Form hatalarını loglayın
            messages.error(request, "Candidate couldn't be added. Please check the errors.")
    else:
        form_candidate = AddNewCandidate()
    
    candidates = Candidate.objects.all()
    return render(request, "newcandidate.html", {"form": form_candidate, "candidates": candidates})
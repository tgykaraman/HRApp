from django.shortcuts import render,redirect,get_object_or_404
from .forms import AddNewEmployee, AddNewJob, AddNewCandidate, SalaryForm, EmployeeForm
from django.urls import reverse 
from .models import Employee, Recruitment, Candidate, Salary
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
        form= AddNewCandidate(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, "Candidate added successfully!")
            return redirect("hr_app:addcandidate")
        else:
            print("Form is not valid:", form.errors)  # Form hatalarını loglayın
            messages.error(request, "Candidate couldn't be added. Please check the errors.")
    else:
        form = AddNewCandidate()
    
    candidates = Candidate.objects.all()
    return render(request, "newcandidate.html", {"form": form, "candidates": candidates})

def jobview(request):
    jobs = Recruitment.objects.all()
    return render(request,"jobs.html",{"jobs":jobs})

def candidateview(request):
    candidates_by_status = {
        'Sourced': Candidate.objects.filter(status='Sourced'),
        'In Progress': Candidate.objects.filter(status='In Progress'),
        'Interview': Candidate.objects.filter(status='Interview'),
        'Hired': Candidate.objects.filter(status='Hired'),
        'Rejected': Candidate.objects.filter(status='Rejected'),
    }
    context = {
        'candidates_by_status': candidates_by_status
    }
    return render(request,"candidates.html",context=context)

def jobdetails(request,id):
    job = Recruitment.objects.get(id=id)
    requirements = [req.strip() for req in job.requirements.split(',')]
    return render(request,"jobdetails.html",{"job":job, "requirements":requirements})

def edit_job(request,id):
    job = get_object_or_404(Recruitment,id=id)
    if request.method == "POST":
        form = AddNewJob(request.POST,instance=job)
        if form.is_valid():
            form.save()
            messages.success(request,"Job edited successfully!")
            jobs = Recruitment.objects.all()
            return render(request,"jobs.html",{"jobs":jobs})
        else:
            messages.error(request,"Job couldn't be edited. Please check the errors.")
    else:
       form = AddNewJob(instance=job)
    return render(request,"editjob.html",{"form":form})

def deletejob(request,id):
    job = Recruitment.objects.get(pk=id)
    Recruitment.objects.filter(id=id).delete()
    return redirect("hr_app:jobs")

def edit_candidate(request,id):
    candidate = get_object_or_404(Candidate,id=id)
    if request.method == "POST":
        form = AddNewCandidate(request.POST,instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request,"Candidate edited successfully!")
            return redirect("hr_app:candidates")
        else:
            messages.error(request,"Candidate couldn't be edited. Please check the errors.")
    else:
       form = AddNewCandidate(instance=candidate)
    return render(request,"editcandidate.html",{"form":form})

def deletecandidate(request,id):
    candidate = Candidate.objects.get(pk=id)
    Candidate.objects.filter(id=id).delete()
    return redirect("hr_app:candidates")

def jobfilter(request):
    jobs = Recruitment.objects.all()
    name_filter = request.GET.get("job_title")
    department_filter = request.GET.get("department")

    if name_filter:
        jobs = jobs.filter(job_title__icontains=name_filter).all()
    if department_filter:
        jobs = jobs.filter(department__icontains=department_filter).all()
    
    context = {"jobs":jobs,
               "name_filter": name_filter,
               "department_filter": department_filter}
    print(f"{name_filter} & {department_filter}")
    return render(request,"jobs.html",context=context)

def export_jobs_to_excel(request):
    jobs = Recruitment.objects.all().values()
    df = pd.DataFrame(jobs)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=jobs.xlsx'
    df.to_excel(response, index=False)
    return response

def export_candidates_to_excel(request):
    candidates = Candidate.objects.all().values()
    df = pd.DataFrame(candidates)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=candidates.xlsx'
    df.to_excel(response, index=False)
    return response

def update_salary(request,id):
    employee = get_object_or_404(Employee,id=id)
    if request.method == "POST":
        employee_form = EmployeeForm(request.POST, instance=employee)
        salary_form = SalaryForm(request.POST)
        if employee_form.is_valid() and salary_form.is_valid():
            employee_form.save()
            salary = salary_form.save(commit=False)
            salary.employee = employee
            salary.save()
            return redirect("hr_app:payrollview")
    else:
        employee_form = EmployeeForm(instance=employee)
        salary_form = SalaryForm()
    context = {
        "employee_form": employee_form,
        "salary_form": salary_form
    }
    return render(request,"updatesalary.html",context)

def payrollview(request):
    employees = Employee.objects.all()
    salaries = Salary.objects.all()
    return render(request,"payroll.html",{"employees":employees, "salaries":salaries})

from django.shortcuts import render,redirect,get_object_or_404
from .forms import AddNewEmployee, AddNewJob, AddNewCandidate, SalaryForm, EmployeeForm, LeaveRequestFormEmployee, LeaveRequestFormAdmin
from django.urls import reverse 
from .models import Employee, Recruitment, Candidate, Salary, Events, LeaveRequest
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login")
def manageemployee(request):
    employees = Employee.objects.all()
    return render(request,"manageemployee.html",{"employees":employees})

@login_required(login_url="/login")
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

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def export_employees_to_excel(request):
    employees = Employee.objects.all().values()
    df = pd.DataFrame(employees)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
    df.to_excel(response, index=False)
    return response

@login_required(login_url="/login")
def deleteemployee(request,id):
    employee = Employee.objects.get(pk=id)
    Employee.objects.filter(id=id).delete()
    return redirect("hr_app:manageemployee")

@login_required(login_url="/login")
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

@login_required(login_url="/login")
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

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def jobview(request):
    jobs = Recruitment.objects.all()
    return render(request,"jobs.html",{"jobs":jobs})

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def jobdetails(request,id):
    job = Recruitment.objects.get(id=id)
    requirements = [req.strip() for req in job.requirements.split(',')]
    return render(request,"jobdetails.html",{"job":job, "requirements":requirements})

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def deletejob(request,id):
    job = Recruitment.objects.get(pk=id)
    Recruitment.objects.filter(id=id).delete()
    return redirect("hr_app:jobs")

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def deletecandidate(request,id):
    candidate = Candidate.objects.get(pk=id)
    Candidate.objects.filter(id=id).delete()
    return redirect("hr_app:candidates")

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def export_jobs_to_excel(request):
    jobs = Recruitment.objects.all().values()
    df = pd.DataFrame(jobs)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=jobs.xlsx'
    df.to_excel(response, index=False)
    return response

@login_required(login_url="/login")
def export_candidates_to_excel(request):
    candidates = Candidate.objects.all().values()
    df = pd.DataFrame(candidates)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=candidates.xlsx'
    df.to_excel(response, index=False)
    return response

@login_required(login_url="/login")
def add_salary(request,id):
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

@login_required(login_url="/login")
def payrollview(request):
    employees = Employee.objects.all()
    salaries = Salary.objects.all()
    return render(request,"payroll.html",{"employees":employees, "salaries":salaries})

@login_required(login_url="/login")
def update_salary(request,employee_id, salary_id):
    employee = get_object_or_404(Employee,id=employee_id)
    salary = get_object_or_404(Salary,id=salary_id)
    if request.method == "POST":
        employee_form = EmployeeForm(request.POST, instance=employee)
        salary_form = SalaryForm(request.POST, instance=salary)
        if employee_form.is_valid() and salary_form.is_valid():
            employee_form.save()
            salary = salary_form.save(commit=False)
            salary.employee = employee
            salary.save()
            return redirect("hr_app:payrollview")
    else:
        employee_form = EmployeeForm(instance=employee)
        salary_form = SalaryForm(instance=salary)
    context = {
        "employee_form": employee_form,
        "salary_form": salary_form
    }
    return render(request,"editsalary.html",context)

@login_required(login_url="/login")
def delete_salary(request,id):
    salary = Salary.objects.get(pk=id)
    Salary.objects.filter(id=id).delete()
    return redirect("hr_app:payrollview")  

@login_required(login_url="/login")
def payrollfilter(request):
    employees = Employee.objects.all()
    salaries = Salary.objects.all()
    name_filter = request.GET.get("name")

    if name_filter:
        employees = employees.filter(name__icontains=name_filter).all()
    
    context = {"employees":employees,
               "salaries":salaries,
               "name_filter": name_filter}
    print(f"{name_filter}")
    return render(request,"payroll.html",context=context)

@login_required(login_url="/login")
def export_payroll_to_excel(request):
    salaries = Salary.objects.all().values()
    df = pd.DataFrame(salaries)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=payroll.xlsx'
    df.to_excel(response, index=False)
    return response

@login_required(login_url="/login")
def schedule(request):  
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'schedule.html',context)

@login_required(login_url="/login")
def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })
    return JsonResponse(out, safe=False) 

@login_required(login_url="/login")
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)

@login_required(login_url="/login")
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)

@login_required(login_url="/login")
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)                                                                                                               
                                          
def login_employee(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                if user.email == 'hradmin@kartek.com.tr':  # HR Admin e-posta adresini kontrol edin
                    return redirect('hr_app:manageemployee')  # HR Admin için yönlendirme
                else:
                    return redirect('hr_app:homeemployee')  # Diğer kullanıcılar için yönlendirme
            else:
                return render(request, 'registration/login.html', {'error': 'Invalid email or password'})
        except User.DoesNotExist:
            return render(request, 'registration/login.html', {'error': 'User does not exist'})
    return render(request, 'registration/login.html')

@login_required(login_url="/login")
def homeemployee(request):
    employee = Employee.objects.get(email=request.user.email)
    return render(request,"homeemployee.html",{"employee":employee})

@login_required(login_url="/login")
def payrollemployee(request):
    employee = Employee.objects.get(email=request.user.email)
    salaries = Salary.objects.filter(employee=employee.id)
    return render(request,"payrollemployee.html",{"employee":employee, "salaries":salaries})

@login_required(login_url="/login")
def add_leave_request(request):
    employee = get_object_or_404(Employee,email=request.user.email)
    if request.method == "POST":
        leave_request_form = LeaveRequestFormEmployee(request.POST)
        if leave_request_form.is_valid():
            leave_request = leave_request_form.save(commit=False)
            leave_request.employee = employee
            leave_request.save()
            print(leave_request_form.errors)
            return redirect("hr_app:timeoffemployee")
    else:
         leave_request_form = LeaveRequestFormEmployee()
    context = {
        "leave_request_form": leave_request_form,
        "employee":employee
    }
    print(leave_request_form.errors)
    return render(request,"leaveformemployee.html",context)  

@login_required(login_url="/login")
def timeoffemployee(request):
    employee = Employee.objects.get(email=request.user.email)
    leave_requests = LeaveRequest.objects.filter(employee=employee.id)
    return render(request,"timeoffemployee.html",{"employee":employee, "leave_requests":leave_requests})

@login_required(login_url="/login")
def add_timeoff(request,id):
    employee = get_object_or_404(Employee,id=id)
    if request.method == "POST":
        leave_form = LeaveRequestFormAdmin(request.POST)
        if leave_form.is_valid():
            leave_form = leave_form.save(commit=False)
            leave_form.employee = employee
            leave_form.save()
            return redirect("hr_app:timeoffadmin")
    else:
        leave_form = LeaveRequestFormAdmin()
    context = {
        "leave_form": leave_form
    }
    return render(request,"leaveformadmin.html",context)

@login_required(login_url="/login")
def timeoffadmin(request):
    employees = Employee.objects.all()
    leave_requests = LeaveRequest.objects.all()
    return render(request,"timeoffadmin.html",{"employees":employees, "leave_requests":leave_requests})

@login_required(login_url="/login")
def edit_timeoff(request,employee_id, leave_id):
    employee = get_object_or_404(Employee,id=employee_id)
    leave = get_object_or_404(LeaveRequest,id=leave_id)
    if request.method == "POST":
        leave_form = LeaveRequestFormAdmin(request.POST, instance=leave)
        if leave_form.is_valid():
            leave = leave_form.save(commit=False)
            leave.employee = employee
            leave.save()
            return redirect("hr_app:timeoffadmin")
    else:
        leave_form = LeaveRequestFormAdmin(instance=leave)
    context = {
        "leave_form": leave_form
    }
    return render(request,"edittimeoff.html",context)

@login_required(login_url="/login")
def delete_timeoff(request,id):
    leave = LeaveRequest.objects.get(pk=id)
    LeaveRequest.objects.filter(id=id).delete()
    return redirect("hr_app:timeoffadmin")

@login_required(login_url="/login")
def timeofffilter(request):
    employees = Employee.objects.all()
    leaves = LeaveRequest.objects.all()
    name_filter = request.GET.get("name")

    if name_filter:
        employees = employees.filter(name__icontains=name_filter).all()
    
    context = {"employees":employees,
               "leaves":leaves,
               "name_filter": name_filter}
    print(f"{name_filter}")
    return render(request,"timeoffadmin.html",context=context)

@login_required(login_url="/login")
def export_timeoff_to_excel(request):
    leaves = LeaveRequest.objects.all().values()
    df = pd.DataFrame(leaves)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=timeoff.xlsx'
    df.to_excel(response, index=False)
    return response
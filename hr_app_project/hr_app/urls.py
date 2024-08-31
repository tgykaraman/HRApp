from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = "hr_app"

urlpatterns = [
    path("", views.manageemployee,name="manageemployee"),
    path("addemployee/",views.AddEmployee,name="addemployee"),
    path("edit_employee/<int:id>/",views.edit_employee,name="edit_employee"),
    path("export/",views.export_employees_to_excel,name="export_excel_employee"),
    path("deleteemployee/<int:id>",views.deleteemployee,name="deleteemployee"),
    path("tablefilter",views.tablefilter,name="tablefilter"),
    path("addjob",views.AddJob, name="addjob"),
    path("addcandidate",views.AddCandidate, name="addcandidate"),
    path("jobs",views.jobview, name="jobs"),
    path("candidates",views.candidateview, name="candidates"),
    path("jobdetails/<int:id>",views.jobdetails, name="jobdetails"),
    path("edit_job/<int:id>/",views.edit_job,name="edit_job"),
    path("deletejob/<int:id>",views.deletejob,name="deletejob"),
    path("edit_candidate/<int:id>/",views.edit_candidate,name="edit_candidate"),
    path("deletecandidate/<int:id>",views.deletecandidate,name="deletecandidate"),
    path("jobfilter",views.jobfilter,name="jobfilter"),
    path("exportjob/",views.export_jobs_to_excel,name="export_excel_job"),
    path("exportcandidate/",views.export_candidates_to_excel,name="export_excel_candidate"),
    path("payrollview/",views.payrollview,name="payrollview"),
    path("add_salary/<int:id>",views.add_salary,name="add_salary"),
    path("update_salary/<int:employee_id>/<int:salary_id>",views.update_salary,name="update_salary"),
    path("delete_salary/<int:id>",views.delete_salary,name="delete_salary"),
    path("payrollfilter",views.payrollfilter,name="payrollfilter"),
    path("exportpayroll/",views.export_payroll_to_excel,name="export_excel_payroll"),
    path('schedule/', views.schedule, name='schedule'), 
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('homeemployee/', views.homeemployee, name="homeemployee"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.login_employee, name='login'),
    path('payrollemployee/', views.payrollemployee, name="payrollemployee"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
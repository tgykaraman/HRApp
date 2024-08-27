from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path("candidates",views.candidateview, name="candidates")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "hr_app"

urlpatterns = [
    path("", views.manageemployee,name="manageemployee"),
    path("addemployee/",views.AddEmployee,name="addemployee")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
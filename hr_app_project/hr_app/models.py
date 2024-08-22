from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import date
# Create your models here.

#Kullanıcı Tablosu
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(help_text="someone@kartek.com",unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(null=True)
    position = models.CharField(max_length=50)
    contract_type = models.CharField(max_length=50)
    hire_date= models.DateField()
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    department = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    birthdate = models.DateField()
    photo = models.ImageField(upload_to="employee_photos/")
    password = models.CharField(max_length=120)
    absence = models.DecimalField(max_digits=4,decimal_places=1,null=True)

    #Şifre hashleme
    def save(self,*args,**kwargs):
        today = date.today()
        employment_duration = today - self.hire_date
        self.password = make_password(self.password)
        if employment_duration.days >= 365:
            self.absence = 14.0
        super().save(*args,**kwargs)

    #Kullanıcının çıktısı
    def __str__(self):
        return self.name
    



from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
# Create your models here.

#Çalışa Tablosu
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    #Şifre hashleme
    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
            today = date.today()
            employment_duration = today - self.hire_date
            if employment_duration.days >= 365:
                self.absence = 14.0
        super().save(*args, **kwargs)
    #Kullanıcının çıktısı
    def __str__(self):
        return self.email
    
class Recruitment(models.Model):
    job_title = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    active_until = models.DateField()
    department = models.CharField(max_length=100)
    contract_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.job_title

class Candidate(models.Model):
    STATUS_CHOICES = [
        ('Sourced', 'Sourced'),
        ('In Progress', 'In Progress'),
        ('Interview', 'Interview'),
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected'),
    ]
    job_title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    source = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Sourced')
    CV = models.FileField(upload_to="cvs/")
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.job_title
    
class Salary(models.Model):
    STATUS_CHOICES = [
        ("",""),
        ("Pending","Pending"),
        ("Paid", "Paid"),
        ("Overdue", "Overdue")
    ]

    MONTH_CHOICES =[
        ("",""),
        ("January","January"),
        ("February","February"),
        ("March","March"),
        ("April","April"),
        ("May","May"),
        ("June","June"),
        ("July","July"),
        ("Augusth","Augusth"),
        ("September","September"),
        ("October","October"),
        ("November","November"),
        ("December","December")
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="salaries")
    month = models.CharField(max_length=100, choices=MONTH_CHOICES,null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,default="Pending")

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
 
    class Meta:  
        db_table = "tblevents"

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected","Rejected")
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_request")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default="Pending",null=True)

    def save(self,*args, **kwargs):
        if self.status == "Approved":
            days_requested = (self.end_date - self.start_date).days
            self.employee.absence  -= days_requested
            if self.employee.absence < -7:
                raise ValueError("Yeterli izin gününüz yok.")
            self.employee.save()
        super().save(*args, **kwargs)
            



    

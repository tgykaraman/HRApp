from typing import Any
from django.forms import ModelForm, ChoiceField
from hr_app.models import Employee, Candidate, Recruitment, Salary
from django import forms
from django.contrib.auth.models import User

class AddNewEmployee(ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ["username","name", "email", "password", "phone", "address", "position", "contract_type", 
                  "hire_date", "salary", "department", "education", "birthdate", "photo", "password_confirm","absence"]
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )   
        employee = super().save(commit=False)
        employee.user = user
        if commit:
            employee.save()
        return employee
    

class AddNewJob(ModelForm):
    class Meta:
        model = Recruitment
        fields = ["job_title","job_type","description","requirements","active_until",
                  "department","contract_type","location"]
        
class AddNewCandidate(ModelForm):
    name = forms.CharField(label="Candidate Name:", max_length=100)
    email = forms.EmailField(label="E-mail:")
    source = forms.ChoiceField(label="Source:", choices=[("Linkedin", "Linkedin"), ("Kariyer.net", "Kariyer.net"), ("Other", "Other")])
    status = forms.ChoiceField(label="Status:", choices=Candidate.STATUS_CHOICES)
    phone = forms.CharField(label="Phone", max_length=100)
    CV = forms.FileField(label="CV:")
    job_title = forms.CharField(label="Job Title:", max_length=100)

    class Meta:
        model = Candidate
        fields = ["job_title", "name", "email", "status", "phone", "source", "CV"]
    
class SalaryForm(ModelForm):
    month = forms.ChoiceField(choices=Salary.MONTH_CHOICES)
    status = forms.ChoiceField(choices=Salary.STATUS_CHOICES)

    class Meta:
        model = Salary
        fields = ["month","status"]

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ["salary"]


    




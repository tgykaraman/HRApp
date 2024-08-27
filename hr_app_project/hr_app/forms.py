from typing import Any
from django.forms import ModelForm
from hr_app.models import Employee, Candidate, Recruitment
from django import forms

class AddNewEmployee(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ["name", "email", "password", "phone", "address", "position", "contract_type", 
                  "hire_date", "salary", "department", "education", "birthdate", "photo", "password_confirm","absence"]
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

class AddNewJob(ModelForm):
    class Meta:
        model = Recruitment
        fields = ["job_title","job_type","description","requirements","active_until",
                  "department","contract_type","location"]
        
class AddNewCandidate(forms.Form):
    job_title = forms.CharField(label="Job Title:", max_length=100)
    name = forms.CharField(label= "Candidate Name:", max_length=100)
    email = forms.EmailField(label="E-mail:")
    source = forms.ChoiceField(label= "Source:",choices=[("Linkedin","Linkedin"),("Kariyer.net","Kariyer.net"),("Other","Other")])
    status = forms.ChoiceField(label="Status:",choices=[("Sourced","Sourced"),("In Progress","In Progress"),("Intwerview","Interview"),
                               ("Hired","Hired"),("Rejected","Rejected")])
    phone = forms.CharField(label="Phone",max_length=100)
    CV = forms.FileField(label="CV:")
    
    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data["status"])>1:
            raise forms.ValidationError("Please select only one option")
        if len(cleaned_data["source"])>1:
            raise forms.ValidationError("Please select only one option")
        return cleaned_data
    
    




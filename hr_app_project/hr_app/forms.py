from django.forms import ModelForm
from hr_app.models import Employee
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
        password = cleaned_data.get("password")  # String olarak key kullanılmalı
        password_confirm = cleaned_data.get("password_confirm")  # String olarak key kullanılmalı

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

        


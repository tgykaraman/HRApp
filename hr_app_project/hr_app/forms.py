from django.forms import ModelForm
from hr_app.models import employee
from django import forms

class AddNewEmployee(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = employee
        fields = ["name", "email", "password","phone","address","position","contract_type","hire_date","salary","department","education",
                  "birthdate","photo"]
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get(password)
        password_confirm = cleaned_data.get(password_confirm)

        if password != password_confirm:
            raise forms.ValidationError("Password do not match")
        
        return cleaned_data
        


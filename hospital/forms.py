from django import forms
from .models import Patient, Service, Bill
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password

class PatientAddForm(forms.ModelForm):
    email = forms.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])

    class Meta:
        model = Patient
        fields = ['name', 'contact_number', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Hides password input in form
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Patient.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken! Please choose a different one")
        return username

    def clean_contact_number(self):
        contact = self.cleaned_data.get("contact_number")
        if not contact.isdigit() or len(contact) != 10:
            raise ValidationError("Contact must be exactly 10 digits")
        return contact  # You forgot to return the validated value

    def save(self, commit=True):
        patient = super().save(commit=False)
        patient.password = make_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            patient.save()
        return patient


class PatientEditForm(forms.ModelForm):
    email = forms.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])

    class Meta:
        model = Patient
        fields = ['name', 'contact_number', 'email','password']

    def save(self, commit=True):
        patient = super().save(commit=False)
        patient.password = make_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            patient.save()
        return patient


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'base_price', 'is_active']

class BillForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Bill
        fields = ['patient', 'services', 'discount','paid']
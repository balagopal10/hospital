from django import forms
from .models import Patient, Service, Bill
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password, check_password

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
        fields = ['name', 'contact_number', 'email','username']

class PatientPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget = forms.PasswordInput(attrs={'placeholder':'Enter Old Password'}),
        label = "Old Password",
        required = True
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Enter New Password'}),
        label="New Password",
        required=True
    )

    confirm_new_password=forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Re-Enter New password'}),
        label="Re-enter New Password",
        required=True
    )

    def __init__(self,patient,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.patient=patient # Store the logged-in patient for password validation

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not check_password(old_password, self.patient.password):
            raise ValidationError("Old password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise ValidationError("New password and Confirm new password do not match.")

        return cleaned_data

    def save(self, commit=True):
        new_password = self.cleaned_data["new_password"]
        self.patient.password = make_password(new_password)  # Hash the new password
        if commit:
            self.patient.save()
        return self.patient
    

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
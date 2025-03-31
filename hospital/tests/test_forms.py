import pytest
from django.core.exceptions import ValidationError
from hospital.forms import (
    PatientAddForm, PatientEditForm, 
    PatientPasswordChangeForm, ServiceForm, BillForm
)
from hospital.models import Patient, Service, Bill
from django.contrib.auth.hashers import check_password,make_password

@pytest.mark.django_db
def test_patient_add_form_valid():
    form_data = {
        "name": "John Doe",
        "username": "johndoe",
        "contact_number": "9876543210",
        "email": "johndoe@example.com",
        "password": "securepassword"
    }
    form = PatientAddForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_patient_add_form_invalid_username():
    # Create a patient first
    Patient.objects.create(
        name="Existing User",
        username="existinguser",
        contact_number="1234567890",
        email="existing@example.com",
        password="hashedpass"
    )

    form_data = {
        "name": "John Doe",
        "username": "existinguser",  # Same username as existing patient
        "contact_number": "9876543210",
        "email": "johndoe@example.com",
        "password": "securepassword"
    }
    form = PatientAddForm(data=form_data)
    assert not form.is_valid()
    assert "This username is already taken! Please choose a different one" in form.errors["username"]


@pytest.mark.django_db
def test_patient_add_form_invalid_contact():
    form_data = {
        "name": "John Doe",
        "username": "johndoe",
        "contact_number": "12345",  # Invalid contact number
        "email": "johndoe@example.com",
        "password": "securepassword"
    }
    form = PatientAddForm(data=form_data)
    assert not form.is_valid()
    assert "Contact must be exactly 10 digits" in form.errors["contact_number"]

@pytest.mark.django_db
def test_patient_edit_form_valid():
    patient = Patient.objects.create(
        name="John Doe",
        username="johndoe",
        contact_number="9876543210",
        email="johndoe@example.com",
        password="securepassword"
    )

    form_data = {
        "name": "John Updated",
        "contact_number": "1122334455",
        "email": "updated@example.com",
        "username": "johndoe"
    }
    form = PatientEditForm(data=form_data, instance=patient)
    assert form.is_valid()


@pytest.mark.django_db
def test_patient_password_change_form_valid():
    patient = Patient.objects.create(
        name="John Doe",
        username="johndoe",
        contact_number="9876543210",
        email="johndoe@example.com",
        password=make_password("hashedpass")  # Store hashed password
    )

    form_data = {
        "old_password": "hashedpass",  # Now it will match after hashing
        "new_password": "newsecurepassword",
        "confirm_new_password": "newsecurepassword"
    }
    form = PatientPasswordChangeForm(patient, data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_patient_password_change_form_invalid_old_password():
    patient = Patient.objects.create(
        name="John Doe",
        username="johndoe",
        contact_number="9876543210",
        email="johndoe@example.com",
        password="hashedpass"
    )

    form_data = {
        "old_password": "wrongpass",  # Incorrect old password
        "new_password": "newsecurepassword",
        "confirm_new_password": "newsecurepassword"
    }
    form = PatientPasswordChangeForm(patient, data=form_data)
    assert not form.is_valid()
    assert "Old password is incorrect." in form.errors["old_password"]

@pytest.mark.django_db
def test_service_form_valid():
    form_data = {
        "name": "Blood Test",
        "base_price": 100.00,
        "is_active": True
    }
    form = ServiceForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_bill_form_valid():
    patient = Patient.objects.create(
        name="John Doe",
        username="johndoe",
        contact_number="9876543210",
        email="johndoe@example.com",
        password="securepassword"
    )
    service1 = Service.objects.create(name="X-Ray", base_price=100, is_active=True)
    service2 = Service.objects.create(name="Blood Test", base_price=50, is_active=True)

    form_data = {
        "patient": patient.id,
        "services": [service1.id, service2.id],
        "discount": 10.00,
        "paid": False
    }
    form = BillForm(data=form_data)
    assert form.is_valid()

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from hospital.models import Patient, Service, Bill

@pytest.mark.django_db
def test_home_page(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_patient_list_view(client):
    response = client.get(reverse("patients_list"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_patient_details_view(client):
    patient = Patient.objects.create(
        name="John Doe", 
        username="johndoe", 
        contact_number="1234567890", 
        email="john@example.com"
    )
    response = client.get(reverse("patient_details", args=[patient.pk]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_patient_add_view_get(client):
    response = client.get(reverse("patient_add"))
    assert response.status_code == 200  # Ensure the form page loads

@pytest.mark.django_db
def test_patient_add_view_post(client):
    form_data = {
        "name": "Alice Smith",
        "username": "alicesmith",
        "contact_number": "9876543210",
        "email": "alice@example.com",
        "password": "securepassword"
    }
    response = client.post(reverse("patient_add"), data=form_data)
    assert response.status_code == 302  # Redirect after successful creation
    assert Patient.objects.filter(username="alicesmith").exists()  # Ensure patient is created

@pytest.mark.django_db
def test_patient_update_view(client):
    patient = Patient.objects.create(
        name="John Doe", 
        username="johndoe", 
        contact_number="1234567890", 
        email="john@example.com"
    )
    response = client.get(reverse("patient_update", args=[patient.pk]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_patient_delete_view(client):
    patient = Patient.objects.create(
        name="John Doe", 
        username="johndoe", 
        contact_number="1234567890", 
        email="john@example.com"
    )
    response = client.post(reverse("patient_delete", args=[patient.pk]))
    assert response.status_code == 302  # Should redirect after deletion
    assert not Patient.objects.filter(pk=patient.pk).exists()

@pytest.mark.django_db
def test_admin_dashboard_requires_login(client):
    response = client.get(reverse("admin_dashboard"))
    assert response.status_code == 302  # Should redirect to login page

@pytest.mark.django_db
def test_admin_dashboard_authenticated(admin_client):
    response = admin_client.get(reverse("admin_dashboard"))
    assert response.status_code == 200  # Should be accessible for logged-in admin

@pytest.mark.django_db
def test_service_list_view(client):
    response = client.get(reverse("service_list"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_service_create_view(client):
    response = client.get(reverse("service_create"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_bill_list_view(client):
    response = client.get(reverse("bill_list"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_bill_create_view(client):
    response = client.get(reverse("bill_create"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_patient_login_view(client):
    response = client.get(reverse("patient_login"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_admin_login_view(client):
    response = client.get(reverse("admin_login"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_logout_view(client):
    response = client.get(reverse("logout"))
    assert response.status_code == 302  # Redirect after logout

@pytest.mark.django_db
def test_patient_dashboard_view(client):
    patient = Patient.objects.create(
        name="John Doe", 
        username="johndoe", 
        contact_number="1234567890", 
        email="john@example.com"
    )
    response = client.get(reverse("patient_dashboard", args=[patient.pk]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_change_patient_password_view(client):
    patient = Patient.objects.create(
        name="John Doe", 
        username="johndoe", 
        contact_number="1234567890", 
        email="john@example.com"
    )
    response = client.get(reverse("change_patient_password", args=[patient.pk]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_patient_by_id_view(client):
    response = client.get(reverse("patient_by_id"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_patients_by_service_and_date_view(client):
    response = client.get(reverse("patients_by_service"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_patients_by_name_view(client):
    response = client.get(reverse("patients_by_name"))
    assert response.status_code == 200

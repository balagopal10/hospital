import pytest
from django.urls import reverse
from hospital.models import Patient, Service, Bill

@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200

# ----------------- Patients CRUD Tests -----------------
@pytest.mark.django_db
def test_patient_list_view(client):
    response = client.get(reverse('patients_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_patient_create_view(client):
    response = client.post(reverse('patient_add'), {
        'name': 'John Doe',
        'username': 'johndoe',
        'contact_number': '1234567890',
        'email': 'johndoe@example.com',
        'password': 'securepass'
    })
    assert response.status_code == 302  # Redirect on success
    assert Patient.objects.count() == 1

@pytest.mark.django_db
def test_patient_details_view(client):
    patient = Patient.objects.create(name='John Doe', username='johndoe', contact_number='1234567890', email='johndoe@example.com', password='securepass')
    response = client.get(reverse('patient_details', args=[patient.pk]))
    assert response.status_code == 200
    assert 'John Doe' in response.content.decode()

@pytest.mark.django_db
def test_patient_update_view(client):
    patient = Patient.objects.create(name='John Doe', username='johndoe', contact_number='1234567890', email='johndoe@example.com', password='securepass')
    response = client.post(reverse('patient_update', args=[patient.pk]), {
        'name': 'Updated Name',
        'username': patient.username,
        'contact_number': patient.contact_number,
        'email': patient.email,
        'password': patient.password
    })
    assert response.status_code == 302
    patient.refresh_from_db()
    assert patient.name == 'Updated Name'

@pytest.mark.django_db
def test_patient_delete_view(client):
    patient = Patient.objects.create(name='John Doe', username='johndoe', contact_number='1234567890', email='johndoe@example.com', password='securepass')
    response = client.post(reverse('patient_delete', args=[patient.pk]))
    assert response.status_code == 302
    assert Patient.objects.count() == 0

# ----------------- Services CRUD Tests -----------------
@pytest.mark.django_db
def test_service_list_view(client):
    response = client.get(reverse('service_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_service_create_view(client):
    response = client.post(reverse('service_create'), {
        'name': 'X-Ray',
        'base_price': 100.00
    })
    assert response.status_code == 302
    assert Service.objects.count() == 1

@pytest.mark.django_db
def test_service_update_view(client):
    service = Service.objects.create(name='X-Ray', base_price=100.00)
    response = client.post(reverse('service_update', args=[service.pk]), {
        'name': 'Updated X-Ray',
        'base_price': 150.00
    })
    assert response.status_code == 302
    service.refresh_from_db()
    assert service.name == 'Updated X-Ray'
    assert service.base_price == 150.00

@pytest.mark.django_db
def test_service_delete_view(client):
    service = Service.objects.create(name='X-Ray', base_price=100.00)
    response = client.post(reverse('service_delete', args=[service.pk]))
    assert response.status_code == 302
    assert Service.objects.count() == 0

# ----------------- Bills CRUD Tests -----------------
@pytest.mark.django_db
def test_bill_list_view(client):
    response = client.get(reverse('bill_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_bill_create_view(client):
    patient = Patient.objects.create(name='John Doe', username='johndoe', contact_number='1234567890', email='johndoe@example.com', password='securepass')
    service = Service.objects.create(name='X-Ray', base_price=100.00)
    response = client.post(reverse('bill_create'), {
        'patient': patient.pk,
        'services': [service.pk],
        'discount': 10.00
    })
    assert response.status_code == 302
    assert Bill.objects.count() == 1

@pytest.mark.django_db
def test_bill_update_view(client):
    patient = Patient.objects.create(name='John Doe', username='johndoe', contact_number='1234567890', email='johndoe@example.com', password='securepass')
    service1 = Service.objects.create(name='X-Ray', base_price=100.00)
    service2 = Service.objects.create(name='Blood Test', base_price=50.00)
    bill = Bill.objects.create(patient=patient, discount=10.00)
    bill.services.add(service1)
    response = client.post(reverse('bill_update', args=[bill.pk]), {
        'patient': patient.pk,
        'services': [service1.pk, service2.pk],
        'discount': 5.00
    })
    assert response.status_code == 302
    bill.refresh_from_db()
    assert bill.discount == 5.00
    assert bill.services.count() == 2

@pytest.mark.django_db
def test_bill_delete_view(client):
    patient = Patient.objects.create(name='John Doe', username='johndoe', contact_number='1234567890', email='johndoe@example.com', password='securepass')
    bill = Bill.objects.create(patient=patient, discount=10.00)
    response = client.post(reverse('bill_delete', args=[bill.pk]))
    assert response.status_code == 302
    assert Bill.objects.count() == 0

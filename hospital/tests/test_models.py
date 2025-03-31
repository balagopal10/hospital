import pytest
from hospital.models import Patient, Service, Bill

@pytest.mark.django_db
def test_create_patient():
    patient = Patient(
    name="John Doe",
    username="johndoe",
    contact_number="9084456738",
    email="johndoe@gmail.com",
    password="johndoe"
    )
    patient.save() 
    assert patient.name == "John Doe"
    assert patient.username == "johndoe"
    assert patient.contact_number == "9084456738"
    assert patient.email == "johndoe@gmail.com"
    assert patient.password == "johndoe"

    assert patient.id is not None  # Ensure an ID is generated
    assert len(patient.id) == 10  # Ensure the ID is 10 characters long
    assert patient.id[:2].isalpha()  # Ensure first 2 characters are letters
    assert patient.id[2:].isdigit()  # Ensure last 8 characters are digits

@pytest.mark.django_db
def test_read_patient():
    patient = Patient.objects.create(name="Jane Doe", username="janedoe", email="janedoe@gmail.com", contact_number="1234567890", password="securepass")
    retrieved_patient = Patient.objects.get(username="janedoe")
    assert retrieved_patient.username == "janedoe"
    assert retrieved_patient.email == "janedoe@gmail.com"

@pytest.mark.django_db
def test_update_patient():
    patient = Patient.objects.create(name="John Doe", username="johndoe", email="johndoe@gmail.com", contact_number="1234567890", password="securepass")
    patient.name = "John Doe Updated"
    patient.save()
    updated_patient = Patient.objects.get(username="johndoe")
    assert updated_patient.name == "John Doe Updated"

@pytest.mark.django_db
def test_delete_patient():
    patient = Patient.objects.create(name="John Doe", username="johndoe", email="johndoe@gmail.com", contact_number="1234567890", password="securepass")
    patient.delete()
    assert Patient.objects.filter(username="johndoe").count() == 0

@pytest.mark.django_db
def test_create_service():
    service = Service(
        name = "Medicine",
        base_price = 50
    )
    service.save()

    assert service.id is not None
    assert service.name == "Medicine"
    assert service.base_price == 50

@pytest.mark.django_db
def test_read_service():
    service = Service.objects.create(name="Blood Test", base_price=50)
    retrieved_service = Service.objects.get(name="Blood Test")
    assert retrieved_service.base_price == 50

@pytest.mark.django_db
def test_update_service():
    service = Service.objects.create(name="X-Ray", base_price=100)
    service.base_price = 120
    service.save()
    updated_service = Service.objects.get(name="X-Ray")
    assert updated_service.base_price == 120

@pytest.mark.django_db
def test_delete_service():
    service = Service.objects.create(name="CT Scan", base_price=500)
    service.delete()
    assert Service.objects.filter(name="CT Scan").count() == 0


@pytest.mark.django_db
def test_create_bill():
    # Create a patient
    patient = Patient.objects.create(name="John Doe", username="johndoe", email="johndoe@example.com", contact_number="1234567890", password="securepass")

    # Create services
    service1 = Service.objects.create(name="X-Ray", base_price=100.00)
    service2 = Service.objects.create(name="Blood Test", base_price=50.00)

    # Create a bill
    bill = Bill.objects.create(patient=patient, discount=10.00)  # 10% discount

    # Add services to the bill
    bill.services.add(service1, service2)

    # Recalculate total after adding services
    bill.total_amount = bill.calculate_total()
    bill.save()

    # Assertions
    assert bill.patient == patient
    assert bill.services.count() == 2
    assert bill.total_amount == 135.00  # (100 + 50) - 10% discount
    assert not bill.paid  # Default is unpaid

    print("✅ test_create_bill passed!")  # Optional for debugging

@pytest.mark.django_db
def test_read_bill():
    patient = Patient.objects.create(name="John Doe", username="johndoe", email="johndoe@gmail.com", contact_number="1234567890", password="securepass")
    bill = Bill.objects.create(patient=patient, total_amount=200)
    retrieved_bill = Bill.objects.get(id=bill.id)
    assert retrieved_bill.total_amount == 200

@pytest.mark.django_db
def test_update_bill():
    patient = Patient.objects.create(name="John Doe", username="johndoe", email="johndoe@gmail.com", contact_number="1234567890", password="securepass")
    bill = Bill.objects.create(patient=patient, total_amount=200)
    bill.paid = True
    bill.save()
    updated_bill = Bill.objects.get(id=bill.id)
    assert updated_bill.paid == True

@pytest.mark.django_db
def test_delete_bill():
    patient = Patient.objects.create(name="John Doe", username="johndoe", email="johndoe@gmail.com", contact_number="1234567890", password="securepass")
    bill = Bill.objects.create(patient=patient, total_amount=200)
    bill.delete()
    assert Bill.objects.filter(id=bill.id).count() == 0


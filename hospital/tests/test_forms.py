import pytest
from hospital.forms import PatientAddForm

@pytest.mark.django_db
def test_valid_patient_form():
    form_data = {
        "name": "John Doe",
        "contact_number": "9084456738",  # Corrected field name
        "email": "johndoe@gmail.com",
        "username": "johndoe",
        "password": "johndoe"
    }
    form = PatientAddForm(data=form_data)
    assert form.is_valid(), form.errors  # Show errors if form validation fails

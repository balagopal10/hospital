import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_patient_list_view():
    client = Client()
    response = client.get(reverse("patients_list"))
    assert response.status_code == 200

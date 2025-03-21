from datetime import datetime
from .models import Patient, Service, Bill

def get_patients_by_service_and_date(service_id, date):
    """
    Retrieve all patients who have used a specific service on a given date.
    
    :param service_id: The ID of the service.
    :param date: The date (YYYY-MM-DD) to filter bills.
    :return: Queryset of Patients.
    """
    service = Service.objects.get(id=service_id)
    
    patients = Patient.objects.filter(
        bill__services=service,
        bill__created_at__date=date
    ).distinct()

    return patients

# Example usage:
date_str = "2025-03-19"  # Example date
service_id = 1  # Replace with the actual service ID
filtered_patients = get_patients_by_service_and_date(service_id, date_str)

for patient in filtered_patients:
    print(patient.name, patient.id)

from django.db import models
import random,string

class Patient(models.Model):
    id = models.CharField(primary_key=True, max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def generate_unique_id(self):
        while True:
            prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
            suffix = ''.join(random.choices(string.digits, k=8))
            new_id = prefix + suffix

            if not Patient.objects.filter(id=new_id).exists():
                return new_id

    def save(self, *args, **kwargs):
        if not self.pk:  # This ensures ID is only generated for new objects
            self.id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.id})"
    

class Service(models.Model):
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        """Calculate total amount after discount"""
        if not self.pk:  # Check if the Bill has been saved before accessing services
            return self.total_amount  # Return default value if not saved yet

        service_total = sum(service.base_price for service in self.services.all())
        discount_amount = (self.discount / 100) * service_total
        return service_total - discount_amount  # Return calculated total

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if it's a new object
        super().save(*args, **kwargs)  # Save first to generate ID

        if not is_new:  # Only calculate total after the first save
            self.total_amount = self.calculate_total()
            super().save(update_fields=["total_amount"])  # Save only total_amount

    def __str__(self):
        return f"Bill {self.id} for {self.patient.name}"

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils.timezone import datetime,now
from django.db.models import Sum
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import Patient, Service, Bill
from .forms import PatientAddForm, PatientEditForm, ServiceForm, BillForm,PatientPasswordChangeForm

# Create your views here.
def home(request):
    return render(request,'base.html')

def patient_list(request):
    patients = Patient.objects.all()
    return render(request,'patients/patients_list.html',{'patients':patients})

def patient_details(request,pk):
    patient = get_object_or_404(Patient,pk=pk)
    return render(request, 'patients/patient_details.html', {'patient' : patient}) 

def patient_add(request):
    if request.method == 'POST':
        form = PatientAddForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request,"Patient Registration Successfull")
            return redirect("home")
    else:
        form = PatientAddForm()
    return render(request,'patients/form.html',{'form':form})

def patient_update(request, pk):
    patient = get_object_or_404(Patient,pk=pk)

    if request.method == 'POST':
        form = PatientEditForm(request.POST, instance=patient)

        if form.is_valid() :
            form.save()
           
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("patient_details", pk)

    else:
        form = PatientEditForm(instance=patient)
       
    return render(request, 'patients/edit_form.html', {'form':form,'patient':patient})

def change_patient_password(request, pk):
    patient = Patient.objects.get(pk=pk)  # Get the patient by ID

    if request.method == "POST":
        form = PatientPasswordChangeForm(patient, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been successfully updated!")
            return redirect("patient_dashboard", pk=patient.pk)  # Redirect to patient dashboard after success
    else:
        form = PatientPasswordChangeForm(patient)

    return render(request, "patients/change_password.html", {"form": form, "patient": patient})


def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patients_list')
    return render(request, 'patients/confirm_delete.html', {'patient': patient})

# def patient_dashboard(request,pk):
#     patient=get_object_or_404(Patient,pk=pk)
#     bills=Bill.objects.filter(patient=patient)
#     return render(request,'patients/patient_dashboard.html',{'patient':patient,'bills':bills})

# ----------------------- Services CRUD -----------------------
def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})



def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'services/form.html', {'form': form})



def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/form.html', {'form': form})



def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'services/confirm_delete.html', {'service': service})

# ----------------------- Bills CRUD -----------------------



def bill_list(request):
    bills = Bill.objects.all()
    return render(request, 'bills/bill_list.html', {'bills': bills})



def bill_create(request):
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)  # Create a Bill instance but do not save yet
            bill.save()  # 🔹 First, save to generate an ID
            
            # 🔹 Now, add services AFTER Bill is saved
            services = form.cleaned_data.get('services', [])
            bill.services.set(services)  # Use `.set()` instead of `.add()`
            
            # 🔹 Manually trigger calculate_total() after adding services
            bill.total_amount = bill.calculate_total()
            bill.save(update_fields=["total_amount"])  # Update only total_amount
            
            return redirect("bill_list")
    else:
        form = BillForm()

    return render(request, "bills/form.html", {"form": form})


def bill_update(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('bill_list')
    else:
        form = BillForm(instance=bill)
        return render(request, 'bills/form.html', {'form': form})



def bill_delete(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        bill.delete()
        return redirect('bill_list')
    return render(request, 'bills/confirm_delete.html', {'bill': bill})

#-----------------------------------------------------------------------------------------------------------------------


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:  # Only allow staff/admin users
            login(request, user)
            return redirect("admin_dashboard")  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid credentials or not an admin.")

    return render(request, "admin/admin_login.html")


@login_required  # Ensure only logged-in admins can access
def admin_dashboard(request):
    if not request.user.is_staff:  # Ensure only admins can access
        return redirect("admin_login")

    today = now().date()

    recent_bills = Bill.objects.order_by('-id')[:5]  # Get the latest 5 bills
    total_bills_today = Bill.objects.filter(created_at__date=today).count()
    total_amount_collected = Bill.objects.filter(paid=True).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_payments = Bill.objects.filter(paid=False).count()

    context = {
        'recent_bills': recent_bills,
        'total_bills_today': total_bills_today,
        'total_amount_collected': total_amount_collected,
        'pending_payments': pending_payments,
    }

    return render(request, 'admin/admin_dashboard.html', context)


def patient_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            patient = Patient.objects.get(username=username)  # Fetch patient by username
            if check_password(password, patient.password):  # Compare hashed password
                request.session["patient_id"] = patient.id  # Store patient ID in session
                return redirect("patient_dashboard", pk=patient.pk)  # Redirect to dashboard
            else:
                messages.error(request, "Invalid password.")
        except Patient.DoesNotExist:
            messages.error(request, "Username does not exist.")

    return render(request, "patients/patient_login.html")


def patient_dashboard(request,pk):
    patient=get_object_or_404(Patient,pk=pk)
    bills=Bill.objects.filter(patient=patient)
    return render(request,'patients/patient_dashboard.html',{'patient':patient,'bills':bills})



def logout_view(request):
    logout(request)  # Clears Django auth session
    request.session.flush()  # Clears patient session
    return redirect("home")  # Redirect to home page

def get_patient_by_id(request):
    patient_id = request.GET.get("id")  # Get ID from search input
    if not patient_id:
        return render(request, "patients/patient_by_id.html", {"error_message": "Please enter a Patient ID."})

    patient = Patient.objects.filter(pk=patient_id).first()  # Try to get the patient

    if patient:
        return redirect("patient_details", pk=patient.pk)  # Redirect to details page
    else:
        return render(request, "patients/patient_by_id.html", {"error_message": "Error! Patient Does not Exist"})


def get_patients_by_service_and_date(request):
    """
    Retrieve all patients who have used a specific service on a given date.
    
    :param service_id: The ID of the service.
    :param date: The date (YYYY-MM-DD) to filter bills.
    :return: Queryset of Patients.
    """
    patients = None  # Default: No filter applied
    services = Service.objects.all()  # Get all available services

    service_id = request.GET.get("service_id")
    filter_date = request.GET.get("date")

    if service_id and filter_date:
        try:
            filter_date = datetime.strptime(filter_date, "%Y-%m-%d").date()
            patients = Patient.objects.filter(
                bill__services__id=service_id,
                bill__created_at__date=filter_date
            ).distinct()  # Avoid duplicate patients
        except ValueError:
            patients = None  # Invalid date format

    context = {
        'services': services,
        'patients': patients,  # Pass filtered patients to template
    }

    return render (request,"patients/patients_by_service_n_date.html",context)

def get_patients_by_name(request):
    name = request.GET.get("name")
    patients = Patient.objects.filter(name=name)
    return render(request,"patients/patients_by_name.html",{'patients':patients,'name':name})
# **Medical Center Billing System - Production Report**  
## **Overview**

The **Medical Center Billing System** is a web-based application that streamlines patient billing and management. It provides features such as:  
- **Patient management** (registration, search, and unique IDs)  
- **Service catalog management** (CRUD operations for services)  
- **Billing system** (invoice generation, discounts, and payment tracking)  
- **Admin dashboard** (financial insights, pending payments, and recent transactions)  

---

## **Project Setup**  

### **1. Prerequisites**  
Ensure you have the following installed before proceeding:  
- **Python 3.8+**  
- **PostgreSQL**  
- **Git**  
- **Virtualenv**  
- **Django 4.x**  

---

### **2. Clone the Repository**  
```sh
git clone https://github.com/balagopal10/hospital.git
cd hospital  


### 3. Set Up Virtual Environment
```sh
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

### 4. Install Dependencies
```sh
pip install -r requirements.txt
```

### 5. Configure Database
- Create a PostgreSQL database:
```sql
CREATE DATABASE medical_billing; /* or any name you like, but make sure to give the same name in your settings.py */
```
- Update `settings.py` with your database credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'medical_billing',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Apply Migrations. (Migrate the default tables to database)
```sh
python manage.py migrate
```

### 7. Create Superuser
```sh
python manage.py createsuperuser
```
Follow the prompts to set up an admin account.

### 8. Run the Server
```sh
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`

## Core Features
# 1. 🏥 Patient Management
      ✅ Register, update, and manage patients
      ✅ Assign unique patient IDs
      ✅ Search for patients

# 2. 💊 Service Catalog
      ✅ Add, update, or delete medical services
      ✅ Set base prices for services

# 3. 💰 Billing System
      ✅ Generate and manage bills
      ✅ Apply discounts
      ✅ Track payments (paid/unpaid)

# 4. 📊 Admin Dashboard
      ✅ View recent bills
      ✅ Monitor total earnings
      ✅ Track pending payments


## Deployment
For production deployment, consider using:
- **Gunicorn** as the WSGI server
- **Nginx** as a reverse proxy
- **PostgreSQL** as the database
- **Docker** for containerization (optional)

## Testing
Run the following command to execute all tests:
```sh
   pytest
```

## Contribution
To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
This project is licensed under the MIT License.

---

For the full source code, visit: [GitHub Repository](https://github.com/balagopal10/hospital.git)

For the list of all API's, visit: [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1CBcuyo14MucagO_DcRgYZwmIy_Xi41ErdoRTlzraLWs/edit?usp=sharing)
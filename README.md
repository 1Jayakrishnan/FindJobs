## 🚀 Features Implemented in FindJobs (Job Portal)

This project includes a complete Job Portal workflow with authentication, job management, and user account handling.

---

### ✅ 1. User Registration (Signup)
- New users can register as **Job Seeker** or **Employee**
- Email-based account creation  
- Secure password hashing

---

### 🔑 2. Login & Authentication
- Login using **JWT Token Authentication**
- Access and refresh tokens implemented
- Protected routes for both Job Seekers and Employees

---

### 👤 3. Profile Creation & Management
- Job Seekers can create/update their profile
- Employees can update their company details
- View user profile information anytime

---

### 🧑‍💼 4. Job Seeker Features
- View **all available jobs**
- Apply for jobs
- View list of **applied jobs**
- Restricted from applying to jobs posted by themselves (security rule)

---

### 🏢 5. Employee Features
- Add new job postings
- Update job details
- Delete jobs
- View list of all jobs created by the employee
- Cannot apply to their own posted jobs

---

### 🔐 6. Password Management
- **Forgot Password** feature implemented
- Email-based **OTP verification**
- Reset password using verified OTP

---

### 🔁 7. Login & Logout
- Token-based logout handling
- Secure token invalidation

---

### ❌ 8. User Account Deletion
- Users can permanently delete their account
- All associated data is safely removed

---

### 🛡️ 9. Security Highlights
- JWT Authentication for secure access
- Role-based access control (Job Seeker / Employee)
- OTP-based identity verification
- Validation checks to prevent misuse (e.g., self-job-application prevention)

---


## 🛠 Tech Stack

### 🔙 Backend
- **Django**
- **Django REST Framework (DRF)**

### 🗄️ Database
- **PostgreSQL**

### 🔐 Authentication
- **JWT Token Authentication** (Access & Refresh Tokens)

### 📧 Email Service
- **SMTP** using Django's Email Backend  
- Used for OTP verification & password reset

### 🛡 Security
- **CORS Headers** enabled for secure cross-origin communication


## 🗄️ Database Models

The project is structured into separate Django apps, each responsible for a core part of the Job Portal.

---

### 🔐 Account App (Authentication & Security)
#### **Core Models**
- **User**  
  Custom user model supporting two roles: *Job Seeker* and *Employer*.  
  Includes JWT-based authentication logic.

- **EmailOTP**  
  Stores OTP codes for email verification and password reset.

---

### 🏢 Employee App (Employer Controls)
#### **Models**
- **JobPostModel**  
  Represents job postings created by employers  
  Includes fields like title, description, skills, experience, salary, etc.

- **CompanyModel**  
  Stores company details for each employer.

- **EventsModel**  
  Optional model for company events, hiring events, announcements, etc.

---

### 👤 JobSeeker App (User Profiles & Applications)
#### **Models**
- **UserProfileModel**  
  Stores additional details for job seekers such as bio, resume, skills, etc.

- **JobApplicationModel**  
  Tracks applications submitted by job seekers  
  Includes job reference, status, timestamps, and applicant info.

---

## 🚀 Project Setup

Follow the steps below to set up and run the FindJobs (Job Portal) project on your local machine.

---

### 📥 1. Clone the Repository
```bash
git clone https://github.com/1Jayakrishnan/FindJobs.git
cd FindJobs

### 🧱 2. Create Virtual Environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

---

### ⚙️ 3. Configure Environment Variables
EMAIL_HOST=your_smtp_host
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_email_password

###🗄️ 4. Database Setup
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user 
python manage.py createsuperuser

### ▶️ 5. Start Development Server
python manage.py runserver

Your API will now be available at:
👉 http://localhost:8000/


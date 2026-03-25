# 🚀 Talent Flow - Job Portal System

**Talent Flow** is a comprehensive, full-stack recruitment platform developed using **Python** and **Django**. It is designed to streamline the hiring process by connecting job seekers with employers through a structured 3-tier user ecosystem.

## 👥 3-Tier User Architecture

The platform is built with specific logic for three distinct user roles:

1.  **Admin (Superuser):** Has full control over the database via the Django Admin Panel to manage users, job categories, and site integrity.
2.  **Employer (Company):** Can create and manage company profiles, post job vacancies, and review incoming applications.
3.  **Job Seeker (Candidate):** Can build a professional profile, manage a list of skills, search for jobs, and track their application status.

---

## 🌟 Key Technical Features

### 🔍 Advanced Search & Filtering
* **Dynamic Querying:** Uses Django `Q` objects to search across Job Titles, Company Names, and Descriptions simultaneously.
* **Custom Salary Logic:** Implemented backend filtering using `Cast` and `Replace` to allow numerical comparisons on salary strings (e.g., filtering for "Minimum 10 LPA").
* **Layered Filters:** Sidebar navigation to refine results by **Job Type** (Full-time, Part-time, Internship) and **Work Mode** (Remote, On-site, Hybrid).

### 📑 Application Management
* **Status Tracking:** Candidates can monitor their application lifecycle (**Pending**, **Accepted**, or **Rejected**).
* **Data Integrity:** Used `unique_together` constraints in the database to prevent duplicate applications for the same job.

### 📟 Performance & UI/UX
* **Django Paginator:** Optimized for speed by limiting listings to **6 jobs per page**.
* **Responsive Design:** A modern, professional UI built with **Bootstrap 5**, ensuring compatibility across mobile and desktop devices.

---

## 🛠️ Technical Stack

* **Backend:** Python 3.10+, Django Web Framework
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
* **Database:** SQLite (Development) / Easily migratable to PostgreSQL
* **Libraries:** Pillow (Image/Logo handling), Django Core (ORM, Auth, Paginator)

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JERIMONSHAJI/Job-Portal-Talen-Flow-.git
   ```
2. **Set up a Virtual Environment:**
   ```bash
   python -m venv env
   # Activate on Windows:
   .\env\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install django pillow
   ```
4. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

---

## 👤 Author
**Jerimon Shaji** *BCA Graduate | Python Django Developer*
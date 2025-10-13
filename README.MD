# 🧩 Custom Django Prototype

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)](https://www.postgresql.org/)

A flexible Django prototype designed for rapid application development and customization.  
This project serves as a starting point for building scalable Django-based management systems or dashboards.

---

## 🚀 Features

- 🧠 Modular architecture (apps, services, templates)
- 📊 Integrated dashboard with Chart.js
- 🔄 CRUD operations for core models
- 🧰 Example models: Product, Stock, Location, Movement
- 🌐 Multi-company / multi-location management support
- ⚙️ Custom services (`service.py`) for clean and optimized business logic
- 🗄️ PostgreSQL database configuration (default)

---

## 🛠️ Tech Stack

- **Backend:** Django 4.x (Python 3.10+)
- **Frontend:** HTML, CSS, JS (with Chart.js)
- **Database:** PostgreSQL
- **Tools:** TablePlus, Django Admin, Virtualenv

---

## ⚙️ Installation

### 🧩 Prerequisites
Make sure you have installed:
- Python 3.10+
- PostgreSQL (with a user and database created)
- Git

---

### 💻 Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/Mountainbluesun/custom-django-prototype.git

# 2. Enter the project folder
cd custom-django-prototype

# 3. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment variables
# Create a .env file in the project root and set:
# -----------------------------------------------
# DEBUG=True
# SECRET_KEY=your-secret-key
# DATABASE_NAME=your_db_name
# DATABASE_USER=your_db_user
# DATABASE_PASSWORD=your_db_password
# DATABASE_HOST=localhost
# DATABASE_PORT=5432
# -----------------------------------------------

# 6. Run migrations
python manage.py migrate

# 7. Start the development server
python manage.py runserver

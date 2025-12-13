Custom Django Prototype

Prototype Django full-stack pour la gestion de stock multi-entreprises, développé comme projet de démonstration technique.

🔗 Demo

👉 https://www.jeremylebrun.dev

## 📸 Screenshots

### Dashboard (environnement Linux)
![Dashboard](screenshots/dashboard.png)

### Gestion des produits
![Produits](screenshots/products.png)


🛠 Stack

Python 3

Django 5

PostgreSQL

HTMX

Chart.js

Gunicorn

Nginx

Ubuntu 24.04 (VPS)

✨ Fonctionnalités

Authentification utilisateur

Gestion multi-entreprises / multi-sites

Produits et stocks par site

Mouvements de stock (entrée / sortie)

Dashboard avec indicateurs et graphiques

Interface dynamique avec HTMX

🗂 Modèle de données (simplifié)

Product

Location

Stock (Product × Location)

Movement (IN / OUT)

🚀 Installation (local)
git clone https://github.com/Mountainbluesun/Custom-Django-Prototype.git
cd Custom-Django-Prototype
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

🧪 Tests
pytest

🌐 Déploiement

Déploiement manuel sur VPS Ubuntu

Gunicorn + Nginx

PostgreSQL

HTTPS (Let’s Encrypt)

Variables sensibles via .env (non versionné)

🔐 Sécurité

DEBUG = False en production

HTTPS obligatoire

Accès base de données local uniquement

Pare-feu UFW
Custom Django Prototype

Prototype Django full-stack pour la gestion de stock multi-entreprises, développé comme projet de démonstration technique.

> Projet personnel Django, en évolution continue.
 Demo

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

## Configuration backups

The files below are intentional backups of stable production configurations:

- `src/config/settings.py.stable`
- `src/config/urls.py.stable`

They were created before production routing changes related to Nginx and
the portfolio project page integration.

These files are **not used by Django at runtime** and are kept only
for reference and rollback purposes.


# 🧭 Custom Django Prototype

Prototype full-stack Django avec gestion multi-entreprises, dashboard dynamique et workflow DevOps complet sur VPS Infomaniak.

## 🚀 Stack technique

- **Framework :** Django 5 + HTMX + Chart.js
- **Base de données :** PostgreSQL
- **Serveur d’app :** Gunicorn
- **Reverse proxy :** Nginx
- **Hébergement :** VPS Ubuntu 24.04 (Infomaniak)
- **Sécurité :** HTTPS Let’s Encrypt, Firewall Infomaniak, sessions sécurisées
- **CI/CD :** Git, SCP, systemctl
- **Outils :** PyCharm, TablePlus

## 💻 Fonctionnalités

- Gestion des produits, stocks et mouvements
- Alertes automatiques sur seuil critique
- Dashboard avec graphiques dynamiques (Chart.js)
- Authentification et espace utilisateur
- Multi-entreprise (Lyon, Londres, Bordeaux, Genève)

## 🛠️ Installation

```bash
git clone https://github.com/Mountainbluesun/Custom-Django-Prototype.git
cd Custom-Django-Prototype
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver

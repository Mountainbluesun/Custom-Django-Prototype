# Fichier : src/config/views.py
from django.shortcuts import render
from core.auth_decorators import login_required

@login_required
def home(request):
    return render(request, "home.html")


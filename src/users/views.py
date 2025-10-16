# Fichier : src/users/views.py

# Django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

# Local imports
from core.auth_decorators import login_required, admin_required
from . import service
from .forms import UserCreationForm, UserEditForm
from .models import User


# ============================================================
# AUTHENTICATION VIEWS
# ============================================================

def login_view(request):
    """Vue de connexion avec authentification Django standard."""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # Utilise le système d'authentification Django
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Django gère automatiquement la session
            login(request, user)
            messages.success(request, "Connexion réussie ✅")
            return redirect("home")
        else:
            messages.error(request, "Identifiants invalides ❌")
            return render(request, "users/login.html", status=401)

    return render(request, "users/login.html")


def logout_view(request):
    """Déconnexion avec système Django standard."""
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect("users:login")


# Alias pour compatibilité avec les tests et URLs existantes
login_debug_view = login_view


# ============================================================
# USER MANAGEMENT VIEWS (CRUD)
# ============================================================

@admin_required
def user_list(request):
    """Liste tous les utilisateurs (admin uniquement)."""
    users = service.list_users()
    return render(request, "users/list.html", {"users": users})


@admin_required
def user_create(request):
    """Création d'un nouvel utilisateur (admin uniquement)."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            service.create_user(form.cleaned_data)
            messages.success(request, "Utilisateur créé avec succès.")
            return redirect("users:list")
    else:
        form = UserCreationForm()

    return render(request, "users/form.html", {"form": form, "mode": "create"})


@admin_required
def user_edit(request, pk):
    """Modification d'un utilisateur existant (admin uniquement)."""
    user = service.get_user(pk)
    if not user:
        raise Http404("Utilisateur non trouvé")

    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            service.update_user(pk, form.cleaned_data)
            messages.success(request, f"L'utilisateur '{user.username}' a été mis à jour.")
            return redirect("users:list")
    else:
        form = UserEditForm(initial={
            'username': user.username,
            'email': user.email
        })

    context = {"form": form, "mode": "edit", "user": user}
    return render(request, "users/form.html", context)


@admin_required
def user_delete(request, pk):
    """Suppression d'un utilisateur (admin uniquement)."""
    user = service.get_user(pk)
    if not user:
        raise Http404("Utilisateur non trouvé.")

    if request.method == "POST":
        service.delete_user(pk)
        messages.success(request, f"L'utilisateur '{user.username}' a été supprimé.")
        return redirect(reverse("users:list"))

    return render(request, "users/confirm_delete.html", {"user": user})


# ============================================================
# PROTECTED ROUTES (EXAMPLES)
# ============================================================

@login_required
def home_view(request):
    """Page d'accueil protégée (utilisateur connecté requis)."""
    return render(request, "home.html")


# ============================================================
# DEBUG VIEWS (Development only)
# ============================================================

@admin_required
def debug_users_view(request):
    """Affiche tous les utilisateurs de la base (DEBUG uniquement)."""
    if not settings.DEBUG:
        raise Http404("Cette vue n'est disponible qu'en mode DEBUG")

    users = User.objects.all()

    html = "<h1>Utilisateurs dans la base de données :</h1><ul>"
    if not users:
        html += "<li>Aucun utilisateur trouvé. La table est vide.</li>"
    else:
        for user in users:
            html += f"<li>ID: {user.id}, Username: {user.username}, Email: {user.email}</li>"
    html += "</ul>"

    return HttpResponse(html)


@admin_required
def session_debug(request):
    """Affiche le contenu de la session (DEBUG uniquement)."""
    if not settings.DEBUG:
        raise Http404("Cette vue n'est disponible qu'en mode DEBUG")

    return HttpResponse(f"<pre>Session : {request.session.get('user')}</pre>")


@admin_required
def debug_auth(request):
    """Affiche les informations d'authentification (DEBUG uniquement)."""
    if not settings.DEBUG:
        raise Http404("Cette vue n'est disponible qu'en mode DEBUG")

    data = {
        "is_authenticated": getattr(request.user, "is_authenticated", None),
        "user_class": request.user.__class__.__name__,
        "user_id": getattr(request.user, "id", None),
        "username": getattr(request.user, "username", None),
        "email": getattr(request.user, "email", None),
        "is_admin": getattr(request.user, "is_admin", None),
        "session_keys": list(request.session.keys()),
        "session_data": dict(request.session),
    }
    return JsonResponse(data, json_dumps_params={'indent': 2})

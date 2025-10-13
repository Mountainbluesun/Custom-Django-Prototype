# Fichier : src/users/views.py


from django.http import Http404

from django.http import HttpResponse
from core.auth_decorators import login_required, admin_required
from .forms import UserCreationForm, UserEditForm, PasswordResetRequestForm, PasswordResetConfirmForm
from .models import User, Company
from . import service

from django.utils.crypto import get_random_string



from django.contrib.auth.hashers import make_password,check_password

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User
from .forms import PasswordResetRequestForm



from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import User
from .forms import UserCreationForm, UserEditForm

from .service import list_users, create_user, get_user, update_user, delete_user
from core.auth_decorators import login_required, admin_required

# ---------------- LOGIN / LOGOUT ----------------

# src/users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        print("--- TENTATIVE DE CONNEXION ---")
        print(f"Username reçu : '{username}'")
        print(f"Password reçu : '{password}'")

        user = User.objects.filter(username=username).first()

        if user:
            print(f"Utilisateur trouvé dans la BDD : {user.username}")
            password_is_valid = check_password(password, user.password_hash)
            print(f"Le mot de passe est-il valide ? : {password_is_valid}")
        else:
            print("Utilisateur non trouvé dans la BDD.")
            password_is_valid = False

        if user and password_is_valid:
            # Stockage sécurisé dans la session
            request.session["user"] = {
                "id": user.id,
                "username": user.username,
                "is_admin": user.is_admin,
                "companies": list(user.companies.values_list('id', flat=True)),
                "is_authenticated": True
            }
            messages.success(request, "Connexion réussie ✅")
            print("✅ Connexion réussie, session créée :", request.session["user"])
            return redirect("home")
        else:
            messages.error(request, "Identifiants invalides ❌")
            print("❌ Connexion échouée")

    return render(request, "users/login.html")


def logout_view(request):
    request.session.flush()  # Supprime toutes les données de session
    messages.info(request, "Vous êtes déconnecté.")
    return redirect("users:login")

# ---------------- EXEMPLES DE VUES ----------------

@login_required
def home_view(request):
    return render(request, "home.html")

@admin_required
def user_list_view(request):
    users = list_users()
    return render(request, "users/list.html", {"users": users})


# --- Vues de gestion des utilisateurs (CRUD) ---

@admin_required
def user_list(request):
    users = service.list_users()
    return render(request, "users/list.html", {"users": users})


@admin_required
def user_create(request):
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
        form = UserEditForm(initial={'username': user.username, 'email': user.email})

    context = {"form": form, "mode": "edit", "user": user}
    return render(request, "users/form.html", context)


@admin_required
def user_delete(request, pk):
    user = service.get_user(pk)
    if not user:
        raise Http404("Utilisateur non trouvé.")

    if request.method == "POST":
        service.delete_user(pk)
        messages.success(request, f"L'utilisateur '{user.username}' a été supprimé.")
        return redirect(reverse("users:list"))

    return render(request, "users/confirm_delete.html", {"user": user})


# Les vues pour le mot de passe oublié ne changent presque pas,
# car elles utilisaient déjà une logique qui s'adapte bien.
# Assurez-vous simplement que les imports et les appels de service sont corrects.


def debug_users_view(request):
    """Affiche les utilisateurs que le serveur voit dans la base de données."""
    from .models import User
    users = User.objects.all()

    html = "<h1>Utilisateurs dans la base de données :</h1><ul>"
    if not users:
        html += "<li>Aucun utilisateur trouvé. La table est vide.</li>"
    else:
        for user in users:
            html += f"<li>ID: {user.id}, Username: {user.username}</li>"
    html += "</ul>"

    return HttpResponse(html)

#def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "password_reset_request.html", {"error": "Email inconnu"})

        token = get_random_string(64)
        PasswordResetToken.objects.create(user=user, token=token)

        reset_url = request.build_absolute_uri(
            reverse("password_reset_confirm", args=[token])
        )

        send_mail(
            "Réinitialisation du mot de passe",
            f"Cliquez ici pour réinitialiser : {reset_url}",
            "no-reply@tonsite.com",
            [email],
        )
        return render(request, "password_reset_done.html")

    return render(request, "password_reset_request.html")


#def password_reset_confirm(request, token):
    try:
        token_obj = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return render(request, "password_reset_invalid.html")

    if request.method == "POST":
        new_password = request.POST.get("password")
        token_obj.user.password = make_password(new_password)
        token_obj.user.save()
        token_obj.delete()
        return redirect("login")

    return render(request, "password_reset_confirm.html", {"token": token})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_debug_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        print("--- DEBUG LOGIN ---")
        print(f"Username reçu : {username}")
        print(f"Password reçu : {password}")

        # Utiliser l'authentification Django
        user = authenticate(request, username=username, password=password)

        if user:
            print(f"Utilisateur authentifié : {user.username}, is_active: {user.is_active}")
            login(request, user)
            messages.success(request, f"Connexion réussie ✅ Bienvenue {user.username}")
            return redirect("home")
        else:
            print("❌ Échec de l'authentification")
            messages.error(request, "Identifiants invalides ❌")

    return render(request, "users/login.html")



from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse

def session_debug(request):
    return HttpResponse(f"Session : {request.session.get('user')}")

import json
from django.http import JsonResponse, HttpResponse

def debug_auth(request):
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
    return HttpResponse(json.dumps(data, indent=2), content_type="application/json")






















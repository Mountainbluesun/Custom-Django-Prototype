import json

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password

from core.auth_decorators import login_required, admin_required
from core.forms import ContactForm
from .forms import UserCreationForm, UserEditForm
from .models import User
from . import service
from .service import list_users

# ---------------- LOGIN / LOGOUT ----------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = User.objects.filter(username=username).first()

        if user:
            print(f"User found in DB: {user.username}")
            password_is_valid = check_password(password, user.password_hash)
            print(f"Is the password valid?: {password_is_valid}")
        else:
            print("User not found in DB.")
            password_is_valid = False

        if user and password_is_valid:
            # Secure storage in the session
            request.session["user"] = {
                "id": user.id,
                "username": user.username,
                "is_admin": user.is_admin,
                "companies": list(user.companies.values_list('id', flat=True)),
                "is_authenticated": True
            }
            messages.success(request, "Login successful ✅")
            print("✅ Login successful, session created:", request.session["user"])
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials ❌")
            print("❌ Login failed")
            return render(request, "users/login.html", status=401)

    return render(request, "users/login.html",{"contact_form": ContactForm()})


def logout_view(request):
    request.session.flush()  # Clears all session data
    messages.info(request, "You have been logged out.")
    return redirect("users:login")

# ---------------- EXAMPLE VIEWS ----------------

@login_required
def home_view(request):
    return render(request, 'home.html')


@admin_required
def user_list_view(request):
    users = list_users()
    return render(request, "users/list.html", {"users": users})


# --- User management views (CRUD) ---

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
            messages.success(request, "User created successfully.")
            return redirect("users:list")
    else:
        form = UserCreationForm()
    return render(request, "users/form.html", {"form": form, "mode": "create"})


@admin_required
def user_edit(request, pk):
    user = service.get_user(pk)
    if not user:
        raise Http404("User not found")

    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            service.update_user(pk, form.cleaned_data)
            messages.success(request, f"User '{user.username}' has been updated.")
            return redirect("users:list")
    else:
        form = UserEditForm(initial={
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'companies': user.companies.all(),
        })

    context = {"form": form, "mode": "edit", "user": user}
    return render(request, "users/form.html", context)


@admin_required
def user_delete(request, pk):
    user = service.get_user(pk)
    if not user:
        raise Http404("User not found.")

    if request.method == "POST":
        service.delete_user(pk)
        messages.success(request, f"User '{user.username}' has been deleted.")
        return redirect(reverse("users:list"))

    return render(request, "users/confirm_delete.html", {"user": user})


# The forgot-password views barely change,
# since they already used logic that adapts well.
# Just make sure the imports and service calls are correct.


def debug_users_view(request):
    """Displays the users the server sees in the database."""
    from .models import User
    users = User.objects.all()

    html = "<h1>Users in the database:</h1><ul>"
    if not users:
        html += "<li>No users found. The table is empty.</li>"
    else:
        for user in users:
            html += f"<li>ID: {user.id}, Username: {user.username}</li>"
    html += "</ul>"

    return HttpResponse(html)

def login_debug_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        # Use Django's authentication
        user = authenticate(request, username=username, password=password)

        if user:
            print(f"Authenticated user: {user.username}, is_active: {user.is_active}")
            login(request, user)
            messages.success(request, f"Login successful ✅ Welcome {user.username}")
            return redirect("home")
        else:
            print("❌ Authentication failed")
            messages.error(request, "Invalid credentials ❌")

    return render(request, "users/login.html")


def session_debug(request):
    return HttpResponse(f"Session: {request.session.get('user')}")


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
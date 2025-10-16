from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

# src/core/auth_decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        if not request.user.is_admin:
            return HttpResponseForbidden("Accès réservé aux administrateurs.")
        return view_func(request, *args, **kwargs)
    return _wrapped



def company_required(company_getter):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("users:login")
            target_company_id = company_getter(request, *args, **kwargs)
            user_companies = request.user.companies.values_list('id', flat=True)
            if target_company_id not in user_companies:
                return HttpResponseForbidden("Accès interdit à cette entreprise.")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

# src/core/auth_decorators.py

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        print(">>> EXECUTING login_required DECORATOR <<<")
        print(">>> [DECORATOR] request.user:", request.user)
        if not request.user.is_authenticated:
            return redirect("users:login")
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        if not request.user.is_admin:  # ⚠️ your User model does have this field
            return HttpResponseForbidden("Access restricted to administrators.")
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
                return HttpResponseForbidden("Access denied for this company.")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
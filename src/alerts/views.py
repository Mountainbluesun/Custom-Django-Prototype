# src/alerts/views.py
from django.shortcuts import render
from core.auth_decorators import login_required
from core.scope import scope_for
from .service import compute_alerts

def _allowed_company_ids(request):
    user = scope_for(request)
    if user.get("is_admin"):
        return None  # admins are not filtered
    return user.get("companies", [])

@login_required
def alerts_list(request):
    ids = _allowed_company_ids(request)
    data = compute_alerts(allowed_company_ids=ids)
    return render(request, "alerts/list.html", {"alerts": data})
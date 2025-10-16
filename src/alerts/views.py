# src/alerts/views.py
from django.shortcuts import render
from core.auth_decorators import login_required
from companies.service import list_companies
from .service import compute_alerts

def _allowed_company_ids(request):
    """Retourne les IDs des entreprises accessibles par l'utilisateur."""
    if request.user.is_admin:
        return [c.id for c in list_companies()]
    return list(request.user.companies.values_list('id', flat=True))

@login_required
def alerts_list(request):
    ids = _allowed_company_ids(request)
    data = compute_alerts(allowed_company_ids=ids)
    return render(request, "alerts/list.html", {"alerts": data})





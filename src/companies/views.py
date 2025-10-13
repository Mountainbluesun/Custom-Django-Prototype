from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages

from core.auth_decorators import login_required, admin_required
from .forms import CompanyForm
from .service import list_companies, create_company, get_company, update_company, delete_company


@login_required
def company_list(request):
    ids = _allowed_company_ids(request)
    print("DEBUG allowed_company_ids:", ids)

    companies = list_companies(ids)
    print(f"DEBUG entreprises trouvées: {companies.count()}")
    for c in companies:
        print(f" - {c.name} (ID: {c.id})")

    return render(request, "companies/list.html", {"companies": companies})


from .models import Company

from companies.models import Company

def _allowed_company_ids(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return []

    # Si l'utilisateur est admin
    if getattr(user, "is_admin", False) or user.is_superuser:
        return list(Company.objects.values_list('id', flat=True))

    # Sinon, récupérer les entreprises associées à l'utilisateur
    return list(user.companies.values_list('id', flat=True))






@admin_required
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            create_company(
                name=form.cleaned_data['name'],
                owner=form.cleaned_data.get('owner')
            )
            messages.success(request, "Entreprise créée.")
            return redirect("companies:list")
    else:
        form = CompanyForm()
    return render(request, "companies/form.html", {"mode": "create", "form": form})


@admin_required
def company_edit(request, company_id: int):
    company = get_company(company_id)
    if not company:
        raise Http404("Entreprise introuvable.")

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            update_company(
                company_id,
                name=form.cleaned_data['name'],
                owner=form.cleaned_data.get('owner')
            )
            messages.success(request, "Entreprise mise à jour.")
            return redirect("companies:list")
    else:
        form = CompanyForm(initial={'name': company.name, 'owner': company.owner})

    return render(request, "companies/form.html", {"mode": "edit", "company": company, "form": form})


@admin_required
def company_delete(request, company_id: int):
    company = get_company(company_id)
    if not company:
        raise Http404("Entreprise introuvable.")

    if request.method == "POST":
        delete_company(company_id)
        messages.success(request, "Entreprise supprimée.")
        return redirect("companies:list")

    return render(request, "companies/confirm_delete.html", {"company": company})

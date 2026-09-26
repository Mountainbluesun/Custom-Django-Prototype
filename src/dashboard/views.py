# File: src/dashboard/views.py
from django.shortcuts import render
from django.utils import timezone
from collections import defaultdict
import datetime
import json
from django.shortcuts import render

from core.auth_decorators import admin_required
from companies.service import list_companies
from catalog.service import list_products
from inventory.service import list_movements, compute_stock
from alerts.service import compute_alerts


@admin_required
def home(request):
    # --- Data for the key figures (KPIs) ---
    all_products = list_products()
    all_companies = list_companies()
    allowed_ids = [c.id for c in all_companies]
    alerts = compute_alerts(allowed_company_ids=allowed_ids)

    context = {
        "product_count": len(all_products),
        "company_count": len(all_companies),
        "alert_count": len(alerts),
    }

    # --- Data for Chart 1: Stock by company ---
    stocks_by_company_data = []
    for company in all_companies:
        total_stock = 0
        company_products = [p for p in all_products if p.company.id == company.id]
        for product in company_products:
            total_stock += compute_stock(product.id)
        stocks_by_company_data.append({"name": company.name, "total": total_stock})
    context["stocks_by_company"] = stocks_by_company_data

    # --- Data for Chart 2: Products on alert ---
    context["alerts_chart"] = [{"name": a.product_name, "qty": a.stock} for a in alerts]

    # --- Data for Chart 3: Monthly activity ---
    movements = list_movements()
    monthly_data = defaultdict(lambda: {'in': 0, 'out': 0})
    six_months_ago = timezone.now() - datetime.timedelta(days=180)

    for m in movements:
        move_date = m.timestamp
        if move_date > six_months_ago:
            month_key = move_date.strftime('%Y-%m')
            if m.kind.lower() in ('in', 'transfer_in'):
                monthly_data[month_key]['in'] += m.quantity
            elif m.kind.lower() in ('out', 'transfer_out'):
                monthly_data[month_key]['out'] += m.quantity

    sorted_months = sorted(monthly_data.keys())
    context["monthly_chart_labels"] = [datetime.datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in sorted_months]
    context["monthly_in_data"] = [monthly_data[m]['in'] for m in sorted_months]
    context["monthly_out_data"] = [monthly_data[m]['out'] for m in sorted_months]

    return render(request, "dashboard/home.html", context)


def test_video(request):
    """
    View to display the video test page
    """
    return render(request, 'video_test.html')
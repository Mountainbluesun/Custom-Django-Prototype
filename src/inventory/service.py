# Fichier : src/inventory/service.py
from typing import List, Optional, Iterable
from django.db.models import Sum
from .models import Movement, Product, Company, User


def list_movements(company_ids: Optional[Iterable[int]] = None, product_id: Optional[int] = None) -> List[Movement]:
    """Retourne une liste de mouvements de stock, potentiellement filtrée."""
    queryset = Movement.objects.select_related('product', 'company', 'user').order_by('-timestamp')

    if company_ids:
        queryset = queryset.filter(company_id__in=company_ids)
    if product_id:
        queryset = queryset.filter(product_id=product_id)

    return list(queryset)


def compute_stock(product_id: int) -> int:
    """Calcule le stock actuel d'un produit en sommant tous ses mouvements."""
    # On calcule la somme des entrées
    total_in = Movement.objects.filter(
        product_id=product_id,
        kind__in=['IN', 'TRANSFER_IN']
    ).aggregate(total=Sum('quantity'))['total'] or 0

    # On calcule la somme des sorties
    total_out = Movement.objects.filter(
        product_id=product_id,
        kind__in=['OUT', 'TRANSFER_OUT']
    ).aggregate(total=Sum('quantity'))['total'] or 0

    return total_in - total_out


def add_in(product_id: int, quantity: int, company_id: int, user_id: Optional[int] = None, note: str = "") -> Movement:
    """Ajoute une entrée de stock."""
    return Movement.objects.create(
        product_id=product_id,
        company_id=company_id,
        user_id=user_id,
        quantity=quantity,
        kind='IN',
        note=note
    )


def add_out(product_id: int, quantity: int, company_id: int, user_id: Optional[int] = None, note: str = "") -> Movement:
    """Ajoute une sortie de stock, en vérifiant si le stock est suffisant."""
    current_stock = compute_stock(product_id)
    if current_stock < quantity:
        raise ValueError("Stock insuffisant pour cette sortie.")

    return Movement.objects.create(
        product_id=product_id,
        company_id=company_id,
        user_id=user_id,
        quantity=quantity,
        kind='OUT',
        note=note
    )


def add_transfer(product_id: int, quantity: int, company_from_id: int, company_to_id: int,
                 user_id: Optional[int] = None, note: str = ""):
    """
    Crée un transfert en générant deux mouvements : une sortie de transfert et une entrée de transfert.
    """
    # On vérifie d'abord si le stock est suffisant (comme le faisait add_out)
    # Note : ce calcul est global. Pour être plus précis, il faudrait calculer le stock par entreprise.
    current_stock = compute_stock(product_id)
    if current_stock < quantity:
        raise ValueError("Stock insuffisant pour réaliser le transfert.")

    # On crée le mouvement de SORTIE de transfert
    Movement.objects.create(
        product_id=product_id,
        company_id=company_from_id,
        user_id=user_id,
        quantity=quantity,
        kind='TRANSFER_OUT',  # <-- Le bon type
        note=note
    )

    # On crée le mouvement d'ENTRÉE de transfert
    Movement.objects.create(
        product_id=product_id,
        company_id=company_to_id,
        user_id=user_id,
        quantity=quantity,
        kind='TRANSFER_IN',  # <-- Le bon type
        note=note
    )
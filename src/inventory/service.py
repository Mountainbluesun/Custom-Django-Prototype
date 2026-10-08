from typing import List, Optional, Iterable
from django.db.models import Sum
from .models import Movement


def list_movements(company_ids: Optional[Iterable[int]] = None, product_id: Optional[int] = None) -> List[Movement]:
    """Returns a list of stock movements, optionally filtered."""
    queryset = Movement.objects.select_related('product', 'company', 'user').order_by('-timestamp')

    # None means "no filter"; an empty list means "no company allowed"
    if company_ids is not None:
        queryset = queryset.filter(company_id__in=company_ids)
    if product_id:
        queryset = queryset.filter(product_id=product_id)

    return list(queryset)


def compute_stock(product_id: int) -> int:
    """Computes the current stock of a product by summing all its movements."""
    # Sum of stock-in movements
    total_in = Movement.objects.filter(
        product_id=product_id,
        kind__in=['IN', 'TRANSFER_IN']
    ).aggregate(total=Sum('quantity'))['total'] or 0

    # Sum of stock-out movements
    total_out = Movement.objects.filter(
        product_id=product_id,
        kind__in=['OUT', 'TRANSFER_OUT']
    ).aggregate(total=Sum('quantity'))['total'] or 0

    return total_in - total_out


def add_in(product_id: int, quantity: int, company_id: int, user_id: Optional[int] = None, note: str = "") -> Movement:
    """Adds a stock-in movement."""
    return Movement.objects.create(
        product_id=product_id,
        company_id=company_id,
        user_id=user_id,
        quantity=quantity,
        kind='IN',
        note=note
    )


def add_out(product_id: int, quantity: int, company_id: int, user_id: Optional[int] = None, note: str = "") -> Movement:
    """Adds a stock-out movement, checking that stock is sufficient."""
    current_stock = compute_stock(product_id)
    if current_stock < quantity:
        raise ValueError("Insufficient stock for this withdrawal.")

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
    Creates a transfer by generating two movements: a transfer-out and a transfer-in.
    """
    # First check whether stock is sufficient (same as add_out)
    # Note: this calculation is global. For more accuracy, stock should be computed per company.
    current_stock = compute_stock(product_id)
    if current_stock < quantity:
        raise ValueError("Insufficient stock to complete the transfer.")

    # Create the transfer-OUT movement
    Movement.objects.create(
        product_id=product_id,
        company_id=company_from_id,
        user_id=user_id,
        quantity=quantity,
        kind='TRANSFER_OUT',  # <-- The correct type
        note=note
    )

    # Create the transfer-IN movement
    Movement.objects.create(
        product_id=product_id,
        company_id=company_to_id,
        user_id=user_id,
        quantity=quantity,
        kind='TRANSFER_IN',  # <-- The correct type
        note=note
    )
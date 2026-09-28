# src/core/scope.py
def scope_for(request):
    """
    Returns the logged-in user's identity and company scope as a dict:
    {"id", "username", "is_admin", "companies", "is_authenticated"}.
    Built from request.user (the mechanism the real login uses).
    Returns {} for anonymous users.
    """
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {}
    return {
        "id": user.id,
        "username": user.username,
        "is_admin": bool(getattr(user, "is_admin", False) or user.is_superuser),
        "companies": list(user.companies.values_list("id", flat=True)),
        "is_authenticated": True,
    }
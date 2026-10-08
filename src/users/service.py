from typing import List, Optional
from .models import User, Company


def list_users() -> List[User]:
    """Returns the list of all users."""
    return User.objects.all()


def get_user(user_id: int) -> Optional[User]:
    """Retrieves a user by their ID."""
    return User.objects.filter(id=user_id).first()


def create_user(data: dict) -> User:
    """Creates a new user in the database."""
    user = User.objects.create(
        username=data['username'],
        email=data.get('email'),
        is_admin=data.get("is_admin", False),
    )
    user.set_password(data["password"])  # 🔒 Secure
    user.save()

    # Assign companies if provided
    if 'companies' in data:
        companies = Company.objects.filter(id__in=data['companies'])
        user.companies.set(companies)

    return user


def update_user(user_id: int, data: dict) -> Optional[User]:
    """Updates a user."""
    user = get_user(user_id)
    if user:
        user.username = data['username']
        user.email = data.get('email')
        user.is_admin = data.get('is_admin', False)
        user.save()
        if 'companies' in data:
            user.companies.set(data['companies'])
    return user



def delete_user(user_id: int) -> bool:
    """Deletes a user."""
    user = get_user(user_id)
    if user:
        user.delete()
        return True
    return False
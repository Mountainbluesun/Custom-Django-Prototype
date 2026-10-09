from users.models import User, OldUser

for old_user in OldUser.objects.all():
    # Check if the user already exists.
    user, created = User.objects.get_or_create(
        username=old_user.username,
        defaults={
            "email": old_user.email or "",
            "is_staff": old_user.is_admin,
            "is_superuser": old_user.is_admin,
            "is_active": old_user.is_active,
        }
    )

    # Applies a hashed password (if it is plaintext, set_password hashes it)
    if old_user.password:
        user.set_password(old_user.password)
    else:
        user.set_password("changeme123")  # temporary password

    # Copy the reset_token if it exists.
    if old_user.reset_token:
        user.reset_token = old_user.reset_token

    # Synchronizes rights
    user.is_staff = old_user.is_admin
    user.is_superuser = old_user.is_admin

    # Saves the user
    user.save()

    # Copy the ManyToMany relationships (companies)
    user.companies.set(old_user.companies.all())
    user.save()

print("✅ Migration complete: all OldUser users have been converted.")

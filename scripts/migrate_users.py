from users.models import User, OldUser

for old_user in OldUser.objects.all():
    # Vérifie si l'utilisateur existe déjà
    user, created = User.objects.get_or_create(
        username=old_user.username,
        defaults={
            "email": old_user.email or "",
            "is_staff": old_user.is_admin,
            "is_superuser": old_user.is_admin,
            "is_active": old_user.is_active,
        }
    )

    # Applique un mot de passe hashé (si c'est du plaintext, set_password le hashe)
    if old_user.password_hash:
        user.set_password(old_user.password_hash)
    else:
        user.set_password("changeme123")  # mot de passe temporaire

    # Copie le reset_token si existant
    if old_user.reset_token:
        user.reset_token = old_user.reset_token

    # Synchronise les droits
    user.is_staff = old_user.is_admin
    user.is_superuser = old_user.is_admin

    # Sauvegarde l'utilisateur
    user.save()

    # Copie les relations ManyToMany (companies)
    user.companies.set(old_user.companies.all())
    user.save()

print("✅ Migration terminée : tous les utilisateurs OldUser ont été convertis.")

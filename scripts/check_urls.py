from django.urls import reverse, NoReverseMatch

# Liste de tuples : (namespace, view_name, args optionnels)
urls_to_check = [
    ("companies", "list"),
    ("companies", "create"),
    ("companies", "edit", [1]),   # ici 1 est un id fictif
    ("companies", "delete", [1]),
    ("users", "login"),
    ("users", "logout"),
]

for entry in urls_to_check:
    namespace = entry[0]
    view_name = entry[1]
    args = entry[2] if len(entry) > 2 else []
    try:
        url = reverse(f"{namespace}:{view_name}", args=args)
        print(f"✅ {namespace}:{view_name} -> {url}")
    except NoReverseMatch:
        print(f"❌ {namespace}:{view_name} introuvable !")

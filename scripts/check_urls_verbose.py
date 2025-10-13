# scripts/check_urls_verbose.py
from django.urls import get_resolver, reverse, NoReverseMatch

print("\n🔍 Vérification détaillée des URLs Django...\n")

resolver = get_resolver()
all_urls = []

def extract_patterns(resolver, parent_app=None):
    """Explore récursivement les namespaces et noms de vue, compatible Django 5+."""
    # Certains éléments du resolver peuvent être des tuples (namespace, nested_resolver)
    namespace_items = getattr(resolver, "namespace_dict", {}).items()

    for namespace, nested in namespace_items:
        # Parfois `nested` est un tuple (namespace, resolver)
        nested_resolver = nested if not isinstance(nested, tuple) else nested[1]
        extract_patterns(nested_resolver, parent_app=namespace)

    for name in resolver.reverse_dict.keys():
        if isinstance(name, str):
            if parent_app:
                all_urls.append(f"{parent_app}:{name}")
            else:
                all_urls.append(name)

# Extraire les patterns
extract_patterns(resolver)

# Vérification de chaque nom d’URL connu
for url_name in sorted(all_urls):
    try:
        if any(word in url_name for word in ["edit", "delete", "detail"]):
            path = reverse(url_name, args=[1])
        else:
            path = reverse(url_name)
        print(f"✅ {url_name} -> {path}")
    except NoReverseMatch:
        print(f"❌ {url_name} -> ERREUR lors du reverse()")

print(f"\n📋 Total des routes trouvées : {len(all_urls)}\n")

from django.urls import get_resolver, reverse, NoReverseMatch

print("\n🔍 Detailed verification of Django URLs...\n")

resolver = get_resolver()
all_urls = []

def extract_patterns(resolver, parent_app=None):
    """Recursively explores namespaces and view names; compatible with Django 5+."""
    # Some elements of the resolver can be tuples.(namespace, nested_resolver)
    namespace_items = getattr(resolver, "namespace_dict", {}).items()

    for namespace, nested in namespace_items:
        # Sometimes `nested` is a tuple.(namespace, resolver)
        nested_resolver = nested if not isinstance(nested, tuple) else nested[1]
        extract_patterns(nested_resolver, parent_app=namespace)

    for name in resolver.reverse_dict.keys():
        if isinstance(name, str):
            if parent_app:
                all_urls.append(f"{parent_app}:{name}")
            else:
                all_urls.append(name)

# Extract patterns
extract_patterns(resolver)

# Verification of each known URL name
for url_name in sorted(all_urls):
    try:
        if any(word in url_name for word in ["edit", "delete", "detail"]):
            path = reverse(url_name, args=[1])
        else:
            path = reverse(url_name)
        print(f"✅ {url_name} -> {path}")
    except NoReverseMatch:
        print(f"❌ {url_name} -> ERROR during reverse()")

print(f"\n📋 Total roads found: {len(all_urls)}\n")

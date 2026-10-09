import os
import re
from django.conf import settings
from django.urls import reverse, NoReverseMatch

print("\n🔍 Global scan of Django templates to detect tags {% url '...' %}...\n")

url_pattern = re.compile(r"{%\s*url\s+['\"]([^'\"]+)['\"]")
found_urls = set()

# 1️⃣ Scan all project template directories
search_paths = [os.path.join(settings.BASE_DIR, app) for app in os.listdir(settings.BASE_DIR) if os.path.isdir(os.path.join(settings.BASE_DIR, app))]

for path in search_paths:
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = url_pattern.findall(content)
                    for m in matches:
                        found_urls.add(m)

print(f"🧾  Tags {{% url %}} detected in {len(found_urls)} models.\n")

# 2️⃣ Verification of found names
def safe_reverse(name):
    try:
        if any(x in name for x in ["edit", "delete", "detail"]):
            return reverse(name, args=[1])
        elif "password_reset_confirm" in name:
            return reverse(name, args=["uidb64", "token"])
        else:
            return reverse(name)
    except NoReverseMatch:
        return None

for name in sorted(found_urls):
    resolved = safe_reverse(name)
    if resolved:
        print(f"✅ {name} -> {resolved}")
    else:
        print(f"⚠️ {name} -> not found or requires dynamic arguments")

print("\n📋 Verification complete.\n")

import os
import re
from django.urls import reverse, NoReverseMatch
from django.conf import settings

# Dossier où sont tes templates
TEMPLATE_DIR = os.path.join(settings.BASE_DIR, "templates")

# Expression régulière pour trouver {% url "..." %}
url_pattern = re.compile(r'{%\s*url\s+"([^"]+)"(?:\s+[^%]+)?\s*%}')

def find_templates(dir_path):
    """Renvoie tous les fichiers .html"""
    for root, _, files in os.walk(dir_path):
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(root, f)

def check_urls_in_templates():
    for template_path in find_templates(TEMPLATE_DIR):
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        urls_found = url_pattern.findall(content)
        for u in urls_found:
            try:
                # On split namespace:view si nécessaire
                if ":" in u:
                    ns, view = u.split(":")
                    url = reverse(u)
                else:
                    url = reverse(u)
                print(f"✅ {u} -> OK")
            except NoReverseMatch:
                print(f"❌ {u} -> introuvable ! (template: {template_path})")

if __name__ == "__main__":
    check_urls_in_templates()

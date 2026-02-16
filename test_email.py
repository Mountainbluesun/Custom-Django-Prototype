import os
import sys
import django
from dotenv import load_dotenv

load_dotenv()


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# On pointe vers le dossier src
SRC_PATH = os.path.join(CURRENT_DIR, 'src')

# On ajoute SRC au début du path Python
sys.path.insert(0, SRC_PATH)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    print("✅ Django est enfin initialisé !")
except Exception as e:
    print(f"❌ Erreur : {e}")
    # Si ça plante ici, on affiche le path pour debugger
    print(f"Path actuel recherché par Python : {sys.path[0]}")
    sys.exit(1)

from django.conf import settings
from django.core.mail import send_mail


try:
    send_mail(
        'Test email',
        'Ceci est un test.',
        settings.DEFAULT_FROM_EMAIL,
        ['no-reply@jeremylebrun.dev'],
        fail_silently=False,
    )
    print("🚀 BRAVO ! L'email est parti.")
except Exception as e:
    print(f"🔥 Erreur SMTP : {e}")
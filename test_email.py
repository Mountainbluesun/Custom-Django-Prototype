import os
import sys
import django
from dotenv import load_dotenv

load_dotenv()


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Point to the src folder
SRC_PATH = os.path.join(CURRENT_DIR, 'src')

# Add SRC to the front of the Python path
sys.path.insert(0, SRC_PATH)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    print("✅ Django is finally initialized!")
except Exception as e:
    print(f"❌ Error: {e}")
    # If it crashes here, print the path for debugging
    print(f"Current path searched by Python: {sys.path[0]}")
    sys.exit(1)

from django.conf import settings
from django.core.mail import send_mail


try:
    send_mail(
        'Test email',
        'This is a test.',
        settings.DEFAULT_FROM_EMAIL,
        ['no-reply@jeremylebrun.dev'],
        fail_silently=False,
    )
    print("🚀 SUCCESS! The email was sent.")
except Exception as e:
    print(f"🔥 SMTP Error: {e}")
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # On récupère les données nettoyées
            nom = form.cleaned_data['nom']
            email_utilisateur = form.cleaned_data['email']
            sujet = form.cleaned_data['sujet']
            message_contenu = form.cleaned_data['message']

            # Préparation de l'email
            sujet_mail = f"Nouveau contact : {sujet}"
            corps_mail = f"De: {nom} ({email_utilisateur})\n\nMessage:\n{message_contenu}"

            try:
                send_mail(
                    sujet_mail,
                    corps_mail,
                    'no-reply@jeremylebrun.dev', # L'expéditeur configuré dans settings
                    ['contact@jeremylebrun.dev'], # Ton adresse de réception
                    fail_silently=False,
                )
                messages.success(request, "Votre message a bien été envoyé !")
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f"Erreur lors de l'envoi : {e}")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
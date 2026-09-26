from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Retrieve the cleaned data
            name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_content = form.cleaned_data['message']

            # Prepare the email
            email_subject = f"New contact: {subject}"
            email_body = f"From: {name} ({user_email})\n\nMessage:\n{message_content}"

            try:
                send_mail(
                    email_subject,
                    email_body,
                    'no-reply@jeremylebrun.dev', # Sender configured in settings
                    ['contact@jeremylebrun.dev'], # Your receiving address
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f"Error while sending: {e}")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
from django import forms

from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    nom = forms.CharField(
        label="Votre nom",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )
    email = forms.EmailField(
        label="Votre Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com'
        })
    )
    sujet = forms.CharField(
        label="Sujet",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Demande de renseignement'
        })
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Comment puis-je vous aider ?',
            'rows': 5
        })
    )
    captcha = CaptchaField(label="Vérification (anti-spam)")